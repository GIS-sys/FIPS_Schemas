import psycopg2
from psycopg2 import pool
import requests
from sshtunnel import SSHTunnelForwarder
import uuid
from contextlib import contextmanager
import time

from src.config import loaded_config
from src.logger import logger


class SingleThreadedTunnelManager:
    """Singleton manager for persistent SSH tunnels (single-threaded)"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    @staticmethod
    def instance():
        """Return the singleton instance."""
        return SingleThreadedTunnelManager()

    def _initialize(self):
        # API tunnel (double hop)
        self.api_tunnel = None
        self.jump_tunnel_api = None

        # First DB tunnel (double hop)
        self.db_adapter_tunnel = None
        self.jump_tunnel_db_adapter = None
        self.db_adapter_pool = None

        # Second DB tunnel (single hop via proxy)
        self.db_appl_tunnel = None
        self.db_appl_pool = None

        # Fixed local ports
        self.API_LOCAL_PORT = loaded_config.api_bind_port  # from config
        self.DB_ADAPTER_LOCAL_PORT = 15432
        self.DB_APPL_LOCAL_PORT = 15433  # fixed port for second DB

    def _recreate_db_adapter(self):
        """Fully recreate the db_adapter tunnel and connection pool."""
        logger.log("ERROR: DB adapter tunnel is not active, recreating...", force_print=True)
        self._stop_tunnels(self.db_adapter_tunnel, self.jump_tunnel_db_adapter)
        if self.db_adapter_pool:
            self.db_adapter_pool.closeall()
            self.db_adapter_pool = None
        self.db_adapter_tunnel = None
        self.jump_tunnel_db_adapter = None
        # Force recreation on next access
        self.get_db_adapter_tunnel()
        self._ensure_db_adapter_pool()

    def _recreate_db_appl(self):
        """Fully recreate the db_appl tunnel and connection pool."""
        logger.log("ERROR: DB appl tunnel is not active, recreating...", force_print=True)
        self._stop_tunnels(self.db_appl_tunnel)
        if self.db_appl_pool:
            self.db_appl_pool.closeall()
            self.db_appl_pool = None
        self.db_appl_tunnel = None
        # Force recreation on next access
        self.get_db_appl_tunnel()
        self._ensure_db_appl_pool()

    def _stop_tunnels(self, *tunnels):
        """Safely stop one or more tunnels"""
        for tunnel in tunnels:
            if tunnel and tunnel.is_active:
                tunnel.stop()
        time.sleep(2)

    # ========== API Tunnel (existing) ==========
    def get_api_tunnel(self):
        """Get or recreate persistent API tunnel (double hop)"""
        if self.api_tunnel and self.api_tunnel.is_active:
            return self.api_tunnel

        self._stop_tunnels(self.api_tunnel, self.jump_tunnel_api)

        jump_tunnel = SSHTunnelForwarder(
            (loaded_config.proxy_ip, 22),
            ssh_username=loaded_config.proxy_ssh_user,
            ssh_password=str(loaded_config.proxy_ssh_password),
            remote_bind_address=(loaded_config.api_ip, 22),
        )
        jump_tunnel.start()

        self.api_tunnel = SSHTunnelForwarder(
            ('localhost', jump_tunnel.local_bind_port),
            ssh_username=loaded_config.api_ssh_user,
            ssh_password=str(loaded_config.api_ssh_password),
            remote_bind_address=(loaded_config.api_ip, loaded_config.api_port),
            local_bind_address=('localhost', self.API_LOCAL_PORT),
        )
        self.api_tunnel.start()
        self.jump_tunnel_api = jump_tunnel
        return self.api_tunnel

    @contextmanager
    def api_connection(self):
        """Context manager for API calls"""
        self.get_api_tunnel()
        try:
            yield
        except Exception:
            if self.api_tunnel and not self.api_tunnel.is_active:
                self._stop_tunnels(self.api_tunnel, self.jump_tunnel_api)
                self.api_tunnel = None
                self.jump_tunnel_api = None
            raise

    # ========== First DB (double hop, existing) ==========
    def get_db_adapter_tunnel(self):
        """Get or recreate persistent DB tunnel (double hop)"""
        if self.db_adapter_tunnel and self.db_adapter_tunnel.is_active:
            return self.db_adapter_tunnel

        self._stop_tunnels(self.db_adapter_tunnel, self.jump_tunnel_db_adapter)
        logger.log("WARNING: DB adapter tunnel is not active, recreating...", force_print=True)

        jump_tunnel = SSHTunnelForwarder(
            (loaded_config.proxy_ip, 22),
            ssh_username=loaded_config.proxy_ssh_user,
            ssh_password=str(loaded_config.proxy_ssh_password),
            remote_bind_address=(loaded_config.db_adapter_ip, 22),
        )
        jump_tunnel.start()

        self.db_adapter_tunnel = SSHTunnelForwarder(
            ('localhost', jump_tunnel.local_bind_port),
            ssh_username=loaded_config.db_adapter_user,
            ssh_password=str(loaded_config.db_adapter_password),
            remote_bind_address=('localhost', loaded_config.db_adapter_port),
            local_bind_address=('localhost', self.DB_ADAPTER_LOCAL_PORT),
        )
        self.db_adapter_tunnel.start()
        self.jump_tunnel_db_adapter = jump_tunnel
        return self.db_adapter_tunnel

    def _ensure_db_adapter_pool(self):
        tunnel = self.get_db_adapter_tunnel()
        current_port = tunnel.local_bind_port
        if self.db_adapter_pool and getattr(self.db_adapter_pool, '_port', None) != current_port:
            self.db_adapter_pool.closeall()
            self.db_adapter_pool = None
        if self.db_adapter_pool is None:
            self.db_adapter_pool = pool.SimpleConnectionPool(
                1, 20,
                host='localhost',
                port=current_port,
                user=loaded_config.db_adapter_user,
                password=loaded_config.db_adapter_password,
                database=loaded_config.db_adapter_dbname
            )
            self.db_adapter_pool._port = current_port

    def get_db_adapter_connection(self):
        try:
            self._ensure_db_adapter_pool()
            return self.db_adapter_pool.getconn()
        except (psycopg2.OperationalError, ConnectionRefusedError, OSError) as e:
            # Tunnel or pool is broken – recreate and retry once
            self._recreate_db_adapter()
            try:
                self._ensure_db_adapter_pool()
                return self.db_adapter_pool.getconn()
            except Exception as retry_error:
                # If still failing, raise the original or new error
                raise RuntimeError(f"Failed to get db_adapter connection after recovery: {retry_error}") from e

    def return_db_adapter_connection(self, conn):
        if self.db_adapter_pool:
            self.db_adapter_pool.putconn(conn)

    @contextmanager
    def adapter_db_connection(self):
        conn = self.get_db_adapter_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.return_db_adapter_connection(conn)

    # ========== Second DB (single hop via proxy) ==========
    def get_db_appl_tunnel(self):
        """Get or recreate persistent second DB tunnel (single hop)"""
        if self.db_appl_tunnel and self.db_appl_tunnel.is_active:
            return self.db_appl_tunnel

        self._stop_tunnels(self.db_appl_tunnel)
        logger.log("WARNING: DB appl tunnel is not active, recreating...", force_print=True)

        self.db_appl_tunnel = SSHTunnelForwarder(
            (loaded_config.proxy_ip, 22),
            ssh_username=loaded_config.proxy_ssh_user,
            ssh_password=str(loaded_config.proxy_ssh_password),
            remote_bind_address=(loaded_config.db_appl_host, loaded_config.db_appl_port),
            local_bind_address=('localhost', self.DB_APPL_LOCAL_PORT),
        )
        self.db_appl_tunnel.start()
        return self.db_appl_tunnel

    def _ensure_db_appl_pool(self):
        tunnel = self.get_db_appl_tunnel()
        current_port = tunnel.local_bind_port
        if self.db_appl_pool and getattr(self.db_appl_pool, '_port', None) != current_port:
            self.db_appl_pool.closeall()
            self.db_appl_pool = None
        if self.db_appl_pool is None:
            self.db_appl_pool = pool.SimpleConnectionPool(
                1, 20,
                host='localhost',
                port=current_port,
                user=loaded_config.db_appl_user,
                password=loaded_config.db_appl_password,
                database=loaded_config.db_appl_dbname
            )
            self.db_appl_pool._port = current_port

    def get_db_appl_connection(self):
        try:
            self._ensure_db_appl_pool()
            return self.db_appl_pool.getconn()
        except (psycopg2.OperationalError, ConnectionRefusedError, OSError) as e:
            # Tunnel or pool is broken – recreate and retry once
            self._recreate_db_appl()
            try:
                self._ensure_db_appl_pool()
                return self.db_appl_pool.getconn()
            except Exception as retry_error:
                # If still failing, raise the original or new error
                raise RuntimeError(f"Failed to get db_appl connection after recovery: {retry_error}") from e

    def return_db_appl_connection(self, conn):
        if self.db_appl_pool:
            self.db_appl_pool.putconn(conn)

    @contextmanager
    def db_appl_connection(self):
        """Context manager for second database connections"""
        conn = self.get_db_appl_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.return_db_appl_connection(conn)

    # ========== Cleanup ==========
    def cleanup(self):
        """Clean shutdown of all tunnels and pools"""
        for pool_attr in ('db_adapter_pool', 'db_appl_pool'):
            pool_obj = getattr(self, pool_attr, None)
            if pool_obj:
                pool_obj.closeall()
                setattr(self, pool_attr, None)

        self._stop_tunnels(
            self.api_tunnel, self.jump_tunnel_api,
            self.db_adapter_tunnel, self.jump_tunnel_db_adapter,
            self.db_appl_tunnel
        )
        self.api_tunnel = self.db_adapter_tunnel = self.db_appl_tunnel = None
        self.jump_tunnel_api = self.jump_tunnel_db_adapter = None


# No global variable; use instance() everywhere
import atexit
atexit.register(SingleThreadedTunnelManager.instance().cleanup)
