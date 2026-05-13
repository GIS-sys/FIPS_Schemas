input("DEBUG importing test_samples")

MC1 = """<?xml version="1.0" encoding="UTF-8"?>
<!-- smev_response -->
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>b077cd84-3959-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>4c81cf3b-8ba9-4575-bc3a-c379c0a96d4e</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_ASYNC_BY_SMEV">
				<ns2:MessageID>b09d7e45-3959-11f1-a763-938a8f3d61d2</ns2:MessageID>
				<ns2:To>eyJtaWQiOiJiMDc3Y2Q4NC0zOTU5LTExZjEtYjhiMi0wMjQyMzMzY2NlNTkiLCJ0Y2QiOiI0YzgxY2YzYi04YmE5LTQ1NzUtYmMzYS1jMzc5YzBhOTZkNGUiLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsImNydCI6IjIwMjYtMDQtMTZUMDk6MDE6MjAuMzE5KzAzOjAwIiwibnMiOiJodHRwOi8vZXBndS5nb3N1c2x1Z2kucnUvZWxrL3N0YXR1cy8xLjAuMiIsInNpZCI6MTkzODAxLCJvcmlkIjpudWxsLCJyZW9sIjowLCJlb2wiOjB9</ns2:To>
				<ns2:AsyncProcessingStatus>
					<ns2:OriginalMessageId>b077cd84-3959-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
					<ns2:StatusCategory>requestIsRejectedBySmev</ns2:StatusCategory>
					<ns2:StatusDetails>Бизнес-данные сообщения не соответствуют схеме, зарегистрированной в СМЭВ. MessageId = b077cd84-3959-11f1-b8b2-0242333cce59</ns2:StatusDetails>
					<ns2:SmevFault xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns3:InvalidContent">
						<Code>028122</Code>
						<Description>SMEV-403: Бизнес-данные сообщения не соответствуют схеме, зарегистрированной в СМЭВ. MessageId = b077cd84-3959-11f1-b8b2-0242333cce59</Description>
						<ns3:ValidationError errorPosition="-1">cvc-datatype-valid.1.2.1: '2026-04-15' is not a valid value for 'dateTime'.</ns3:ValidationError>
						<ns3:ValidationError errorPosition="-1">cvc-type.3.1.3: The value '2026-04-15' of element 'ns0:statusDate' is not valid.</ns3:ValidationError>
					</ns2:SmevFault>
				</ns2:AsyncProcessingStatus>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>b09d7e45-3959-11f1-a763-938a8f3d61d2</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>SMEV</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T09:01:20.319+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T09:01:35.327+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>BakE0MG7o0f7YmUwi5gmFrI2AAX3Xs5mpheQE4BLnSk=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>V7Cc5W00wMVnUfVnycA3OjQSqDgkkrBxNbQjBGiDXTA2IFmc52B0p7fH2F/odn65fYrL/wcQ8NwEs2IwhAZpDQ==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC2 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>847c894b-395a-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>6324aae5-d492-469f-9f46-6b650592e2c0</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_ASYNC_BY_SMEV">
				<ns2:MessageID>84cbe25f-395a-11f1-baef-6b0e535a32af</ns2:MessageID>
				<ns2:To>eyJtaWQiOiI4NDdjODk0Yi0zOTVhLTExZjEtYjhiMi0wMjQyMzMzY2NlNTkiLCJ0Y2QiOiI2MzI0YWFlNS1kNDkyLTQ2OWYtOWY0Ni02YjY1MDU5MmUyYzAiLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsImNydCI6IjIwMjYtMDQtMTZUMDk6MDc6MTYuMjk5KzAzOjAwIiwibnMiOiJodHRwOi8vZXBndS5nb3N1c2x1Z2kucnUvZWxrL3N0YXR1cy8xLjAuMiIsInNpZCI6MTkzODAxLCJvcmlkIjpudWxsLCJyZW9sIjowLCJlb2wiOjB9</ns2:To>
				<ns2:AsyncProcessingStatus>
					<ns2:OriginalMessageId>847c894b-395a-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
					<ns2:StatusCategory>requestIsRejectedBySmev</ns2:StatusCategory>
					<ns2:StatusDetails>Бизнес-данные сообщения не соответствуют схеме, зарегистрированной в СМЭВ. MessageId = 847c894b-395a-11f1-b8b2-0242333cce59</ns2:StatusDetails>
					<ns2:SmevFault xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns3:InvalidContent">
						<Code>028122</Code>
						<Description>SMEV-403: Бизнес-данные сообщения не соответствуют схеме, зарегистрированной в СМЭВ. MessageId = 847c894b-395a-11f1-b8b2-0242333cce59</Description>
						<ns3:ValidationError errorPosition="-1">cvc-datatype-valid.1.2.1: '5949=0' is not a valid value for 'integer'.</ns3:ValidationError>
						<ns3:ValidationError errorPosition="-1">cvc-type.3.1.3: The value '5949=0' of element 'ns0:status' is not valid.</ns3:ValidationError>
					</ns2:SmevFault>
				</ns2:AsyncProcessingStatus>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>84cbe25f-395a-11f1-baef-6b0e535a32af</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>SMEV</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T09:07:16.299+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T09:07:46.534+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>R/2ANWySDJ2o/0WBMPQu41HXC8YcFsREdSKWSjBI97Y=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>Cn3SUl0a8U4gDD1z8fpksDoBl7vBWbzjUTlrV4GyobwELD41cLWikNXm+AuqHrtGRHmlxHx3WrW1xFEzqpS2cA==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC3 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>d790b1bd-395a-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>7c4d1afa-d785-4cf8-ad29-1005a66c713b</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>d884886c-395a-11f1-a6ab-b6df272c7906</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiZDc5MGIxYmQtMzk1YS0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiN2M0ZDFhZmEtZDc4NS00Y2Y4LWFkMjktMTAwNWE2NmM3MTNiIiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<orderNumber>1999880001</orderNumber>
									<status>5</status>
									<message>Incorrect request parameters</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>d884886c-395a-11f1-a6ab-b6df272c7906</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T09:09:36.871+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T09:10:34.470+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>JgH26m56FWdklmH6PEjcdBe0mHeLiWzfYvO0hsnIKgI=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>qvy1do3lfeDdDGCgMM0/cU7VuJ0dJva3NTmCTg911M3S4STKYh5Oi8LV/L2I3inAbhmJNHRLQ6Dp+i4AkHGAfA==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>MIII9DCCCKGgAwIBAgIRAu1s4gA3szG4SaWpjU5OezswCgYIKoUDBwEBAwIwggGBMRUwEwYFKoUDZAQSCjc3MDcwNDkzODgxGDAWBgUqhQNkARINMTAyNzcwMDE5ODc2NzELMAkGA1UEBhMCUlUxKTAnBgNVBAgMIDc4INCh0LDQvdC60YIt0J/QtdGC0LXRgNCx0YPRgNCzMSYwJAYDVQQHDB3QodCw0L3QutGCLdCf0LXRgtC10YDQsdGD0YDQszGBnjCBmwYDVQQJDIGT0LzRg9C90LjRhtC40L/QsNC70YzQvdGL0Lkg0L7QutGA0YPQsyDQodC80L7Qu9GM0L3QuNC90YHQutC+0LUg0JLQnS7QotCV0KAu0JMuLCDQodC40L3QvtC/0YHQutCw0Y8g0L3QsNCx0LXRgNC10LbQvdCw0Y8sINC00L7QvCAxNCwg0LvQuNGC0LXRgNCwINCQMSYwJAYDVQQKDB3Qn9CQ0J4gItCg0L7RgdGC0LXQu9C10LrQvtC8IjElMCMGA1UEAwwc0KLQtdGB0YLQvtCy0YvQuSDQo9CmINCg0KLQmjAeFw0yNTA4MTIxMzM0MjRaFw0yNjA4MTIxMzQ0MjRaMIIBvjEVMBMGBSqFA2QEEgo3NzEwNDc0Mzc1MRIwEAYJKoZIhvcNAQkCDANERVYxIDAeBgkqhkiG9w0BCQEWEXNkQHNjLm1pbnN2eWF6LnJ1MRgwFgYFKoUDZAESDTEwNDc3MDIwMjY3MDExGTAXBgNVBAoMENCc0LjQvdGG0LjRhNGA0YsxTTBLBgNVBAkMRNCf0YDQtdGB0L3QtdC90YHQutCw0Y8g0L3QsNCxLiwg0LQuIDEwLCDRgdGC0YAuIDIsIElRLdC60LLQsNGA0YLQsNC7MRUwEwYDVQQHDAzQnNC+0YHQutCy0LAxHDAaBgNVBAgMEzc3INCzLiDQnNC+0YHQutCy0LAxCzAJBgNVBAYTAlJVMYGoMIGlBgNVBAMMgZ3QnNC40L3QuNGB0YLQtdGA0YHRgtCy0L4g0YbQuNGE0YDQvtCy0L7Qs9C+INGA0LDQt9Cy0LjRgtC40Y8sINGB0LLRj9C30Lgg0Lgg0LzQsNGB0YHQvtCy0YvRhSDQutC+0LzQvNGD0L3QuNC60LDRhtC40Lkg0KDQvtGB0YHQuNC50YHQutC+0Lkg0KTQtdC00LXRgNCw0YbQuNC4MGYwHwYIKoUDBwEBAQEwEwYHKoUDAgIkAAYIKoUDBwEBAgIDQwAEQBhe7pMvFyU5u2cfvlZDP8p1uOBzFBA8w2MUwI3UJ8eS9hPbSV2pZmhkOlQit9NWHBYyO5EQYgZONaTwsQZZ3UyjggSqMIIEpjAOBgNVHQ8BAf8EBAMCA/gwHQYDVR0OBBYEFPsLxD95pbiL65oM7SOykYP2tx34MB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEFBQcDBDBUBggrBgEFBQcBAQRIMEYwRAYIKwYBBQUHMAKGOGh0dHA6Ly9jZXJ0ZW5yb2xsLnRlc3QuZ29zdXNsdWdpLnJ1L2NkcC90ZXN0X2NhX3J0azMuY2VyMB0GA1UdIAQWMBQwCAYGKoUDZHEBMAgGBiqFA2RxAjArBgNVHRAEJDAigA8yMDI1MDgxMjEzMzQyM1qBDzIwMjYwODEyMTMzNDIzWjCCATcGBSqFA2RwBIIBLDCCASgMMiLQmtGA0LjQv9GC0L7Qn9GA0L4gQ1NQIDQuMCBSNCIgKNCy0LXRgNGB0LjRjyA0LjApDCwi0JrRgNC40L/RgtC+0J/RgNC+INCj0KYiICjQstC10YDRgdC40LggMi4wKQxh0KHQtdGA0YLQuNGE0LjQutCw0YLRiyDRgdC+0L7RgtCy0LXRgtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDQodCkLzEyNC0zOTcxINC+0YIgMTUuMDEuMjAyMQxh0KHQtdGA0YLQuNGE0LjQutCw0YLRiyDRgdC+0L7RgtCy0LXRgtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDQodCkLzEyOC00Mzc2INC+0YIgMjguMTAuMjAyMjA9BgUqhQNkbwQ0DDIi0JrRgNC40L/RgtC+0J/RgNC+IENTUCA0LjAgUjQiICjQstC10YDRgdC40Y8gNC4wKTBlBgNVHR8EXjBcMFqgWKBWhlRodHRwOi8vY2VydGVucm9sbC50ZXN0Lmdvc3VzbHVnaS5ydS9jZHAvYjBmZDhlYjk1OWQ5NDg5ZDViN2I0YzE0M2EwNmNhZDc5NTJhMDc0NC5jcmwwDAYFKoUDZHIEAwIBADCCAcMGA1UdIwSCAbowggG2gBSw/Y65WdlInVt7TBQ6BsrXlSoHRKGCAYmkggGFMIIBgTEVMBMGBSqFA2QEEgo3NzA3MDQ5Mzg4MRgwFgYFKoUDZAESDTEwMjc3MDAxOTg3NjcxCzAJBgNVBAYTAlJVMSkwJwYDVQQIDCA3OCDQodCw0L3QutGCLdCf0LXRgtC10YDQsdGD0YDQszEmMCQGA1UEBwwd0KHQsNC90LrRgi3Qn9C10YLQtdGA0LHRg9GA0LMxgZ4wgZsGA1UECQyBk9C80YPQvdC40YbQuNC/0LDQu9GM0L3Ri9C5INC+0LrRgNGD0LMg0KHQvNC+0LvRjNC90LjQvdGB0LrQvtC1INCS0J0u0KLQldCgLtCTLiwg0KHQuNC90L7Qv9GB0LrQsNGPINC90LDQsdC10YDQtdC20L3QsNGPLCDQtNC+0LwgMTQsINC70LjRgtC10YDQsCDQkDEmMCQGA1UECgwd0J/QkNCeICLQoNC+0YHRgtC10LvQtdC60L7QvCIxJTAjBgNVBAMMHNCi0LXRgdGC0L7QstGL0Lkg0KPQpiDQoNCi0JqCEQLRkKkAiLBYlkt8lE/Q3xYXMAoGCCqFAwcBAQMCA0EAYHMbP9h8/c8bC89mLEeQ2rqvfELBas8rt+QYSy/Dy0w3AWqwXJ83myM8wwKqCHTJ2Z0MY7U66QlBY7NtxUAcjg==</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>TG6vAadEpQ+mejKZvOUixE+mLWz1QDuX+d5Zn6Cvgwg=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>u7tsmjibsDy9y7CARc6rZiu6npf2CsSwX2TVngZBV7qXVFkuqxIznXFvrSe/qbhJFt1c25rieLBK6UPFUAJoDg==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC4 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>d99dcdaa-395f-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>9d80eeb5-b3c5-440b-b08d-5d1d755f21e9</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>da193fee-395f-11f1-a6ab-b6df272c7906</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiZDk5ZGNkYWEtMzk1Zi0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiOWQ4MGVlYjUtYjNjNS00NDBiLWIwOGQtNWQxZDc1NWYyMWU5IiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<orderNumber>1999880001</orderNumber>
									<status>4</status>
									<message>Status not found</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>da193fee-395f-11f1-a6ab-b6df272c7906</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T09:45:27.000+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T09:45:34.460+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>smendNZswjdCTK6pvXawj+BL+U8jgMWwJ8IL1UNFtnw=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>qcGCm7JJCVHJK77sM9y/AMC8xXMDA80Lsh2yJYtSu9LD7LVdx08qMxjCO7p+hjKHIw7rzApaEUgpwbcuzAvXTQ==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>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</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>9VTPuP13h5DxslTeFRzWuNurIWg3SHCFz2YjOXnPHCA=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>7DRt1wLb/WqEgR0h7d5UJ9Rs+z6StQ8FndJVsOqq1fEZEXI19mLR5LWvCQ/k6otf05S4FhfrVWVEge7ejWqq4g==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC5 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>c8fb9dab-3961-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>230e458c-fa56-4208-8db6-95f294b1383a</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>c9812139-3961-11f1-a6ab-b6df272c7906</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiYzhmYjlkYWItMzk2MS0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiMjMwZTQ1OGMtZmE1Ni00MjA4LThkYjYtOTVmMjk0YjEzODNhIiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<orderNumber>1999880001</orderNumber>
									<status>34</status>
									<message>Order already exists</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>c9812139-3961-11f1-a6ab-b6df272c7906</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T09:59:18.185+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T09:59:34.388+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>l7Tp7Ajy/8cRHPhJgNzbSGxB06BFoG3rDeNtDBOIrx0=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>UQ0l0Zrw+ov2/PNbnTxcVKdN7JfEIUJwh+gdWgpzQ2aJUwATEBeqx8pq34tRyPZtsKRbfSiOZ1EFnwXyKjyieA==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>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</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>qtBB5fIhuU/tx7PAkR9VM9NwIfTRC/HVEwoCngPf2ZI=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>iFr3rAyz92v1VoxWSOA08nDS4vpf7xXn9XKXHbbBieLe36alIMo7y+n0xCfFgWEwuC/mQ7Eipw7ejfTSq0H5Mg==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC6 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>bf74784b-3964-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>20a43961-1bb0-424a-ae40-9fcdb844da9d</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>c062f75f-3964-11f1-9205-b68311fca2ed</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiYmY3NDc4NGItMzk2NC0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiMjBhNDM5NjEtMWJiMC00MjRhLWFlNDAtOWZjZGI4NDRkYTlkIiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<orderNumber>1999880001</orderNumber>
									<status>31</status>
									<message>Incorrect order status specified</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>c062f75f-3964-11f1-9205-b68311fca2ed</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T10:20:31.337+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T10:20:33.321+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>st6Fbbfi4Cip4tUSFk0UGuafmn6Nank7hqYOxb1m8uo=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>2ivESRlhH9SgtobE4LFBnJna0u5JMFWd3t+klrnd0MvFvmQiPV/VJt2P0i0WEi4s1jgxovbYiBGUQTdKVtHrfA==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>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</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>fYcnrgEb/nikDp//lXqArzwdj6bZWzbF9VDtDPUoSfc=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>IG4dIknuCz5Bgr4iA2WykHyION+OU2q6rbKqdgU44YcSezzXiF7XIcrjzvuGRZ4uIjL+9FTIPvgVOFKdfH46Sg==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC7 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>c4a90a37-39a7-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>a6906ec5-d1dc-40be-bfd0-e50a1dd41ad0</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>c5a03aec-39a7-11f1-9205-b68311fca2ed</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiYzRhOTBhMzctMzlhNy0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiYTY5MDZlYzUtZDFkYy00MGJlLWJmZDAtZTUwYTFkZDQxYWQwIiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<elkOrderNumber>0</elkOrderNumber>
									<orderNumber>1999880003</orderNumber>
									<status>13</status>
									<message>Incorrect eServiceCode or serviceTargetCode</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>c5a03aec-39a7-11f1-9205-b68311fca2ed</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T18:20:16.397+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T18:20:33.641+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>+S/wEOmADrG+Nu9tpw0SGM2hKnD1Kt56Ez0FCQjBfpg=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>DjPrNzH1VKEIGgHVKHXdVAfPhzZ4Rze8DLFkizCrCTEY33OM548voZNcpg5zdNAx2Zug7bCCiey9UjQoNMHg5w==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>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</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>NAb+b4q6gHH01tpaOwYy3VOW9IBPSi0oHVI5Ho7G/YY=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>h5v/BNuSRHvxXKmwjXwMRYkm8hGvy5aTIgpD4I/CQAOXBsxzk+QGxEkhn6zx2FWW6qIlRut7QWn03UjCrm4ZJg==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>MIIIczCCCCCgAwIBAgIRAsbmsQATs1q5T+N9Z5wv3AIwCgYIKoUDBwEBAwIwggGBMRUwEwYFKoUDZAQSCjc3MDcwNDkzODgxGDAWBgUqhQNkARINMTAyNzcwMDE5ODc2NzELMAkGA1UEBhMCUlUxKTAnBgNVBAgMIDc4INCh0LDQvdC60YIt0J/QtdGC0LXRgNCx0YPRgNCzMSYwJAYDVQQHDB3QodCw0L3QutGCLdCf0LXRgtC10YDQsdGD0YDQszGBnjCBmwYDVQQJDIGT0LzRg9C90LjRhtC40L/QsNC70YzQvdGL0Lkg0L7QutGA0YPQsyDQodC80L7Qu9GM0L3QuNC90YHQutC+0LUg0JLQnS7QotCV0KAu0JMuLCDQodC40L3QvtC/0YHQutCw0Y8g0L3QsNCx0LXRgNC10LbQvdCw0Y8sINC00L7QvCAxNCwg0LvQuNGC0LXRgNCwINCQMSYwJAYDVQQKDB3Qn9CQ0J4gItCg0L7RgdGC0LXQu9C10LrQvtC8IjElMCMGA1UEAwwc0KLQtdGB0YLQvtCy0YvQuSDQo9CmINCg0KLQmjAeFw0yNTA3MDcxMDM3NDNaFw0yNjA3MDcxMDQ3NDNaMIIBPTEVMBMGBSqFA2QEEgo1MDQ3MDUzOTIwMRowGAYJKoZIhvcNAQkCDAvQotCh0JzQrdCSMzErMCkGCSqGSIb3DQEJARYcVGF0eWFuYS5ub3ZpY2hrb3ZhQHJ0bGFicy5ydTEYMBYGBSqFA2QBEg0xMDM1MDA5NTY3NDUwMR0wGwYDVQQKDBTQkNCeICLQoNCiINCb0LDQsdGBIjEwMC4GA1UECQwn0KPQm9CY0KbQkCDQn9Cg0J7Qm9CV0KLQkNCg0KHQmtCQ0K8sIDIzMRMwEQYDVQQHDArQpdC40LzQutC4MS8wLQYDVQQIDCY1MCDQnNC+0YHQutC+0LLRgdC60LDRjyDQvtCx0LvQsNGB0YLRjDELMAkGA1UEBhMCUlUxHTAbBgNVBAMMFNCQ0J4gItCg0KIg0JvQsNCx0YEiMGYwHwYIKoUDBwEBAQEwEwYHKoUDAgIkAAYIKoUDBwEBAgIDQwAEQHq4oaVgrHEYvykxjLPKyAFHAyGPkB5ieKuiXTHzEh84ul1EB8z8rl13lCkgMKRrn4EDsqY78O+7ni/xd03A+qSjggSqMIIEpjAOBgNVHQ8BAf8EBAMCA/gwHQYDVR0OBBYEFCv1QLkOHgNQPPWEQwsmDx2CuqklMB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEFBQcDBDBUBggrBgEFBQcBAQRIMEYwRAYIKwYBBQUHMAKGOGh0dHA6Ly9jZXJ0ZW5yb2xsLnRlc3QuZ29zdXNsdWdpLnJ1L2NkcC90ZXN0X2NhX3J0azMuY2VyMB0GA1UdIAQWMBQwCAYGKoUDZHEBMAgGBiqFA2RxAjArBgNVHRAEJDAigA8yMDI1MDcwNzEwMzc0M1qBDzIwMjYwNzA3MTAzNzQzWjCCATcGBSqFA2RwBIIBLDCCASgMMiLQmtGA0LjQv9GC0L7Qn9GA0L4gQ1NQIDQuMCBSNCIgKNCy0LXRgNGB0LjRjyA0LjApDCwi0JrRgNC40L/RgtC+0J/RgNC+INCj0KYiICjQstC10YDRgdC40LggMi4wKQxh0KHQtdGA0YLQuNGE0LjQutCw0YLRiyDRgdC+0L7RgtCy0LXRgtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDQodCkLzEyNC0zOTcxINC+0YIgMTUuMDEuMjAyMQxh0KHQtdGA0YLQuNGE0LjQutCw0YLRiyDRgdC+0L7RgtCy0LXRgtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDQodCkLzEyOC00Mzc2INC+0YIgMjguMTAuMjAyMjA9BgUqhQNkbwQ0DDIi0JrRgNC40L/RgtC+0J/RgNC+IENTUCA0LjAgUjQiICjQstC10YDRgdC40Y8gNC4wKTBlBgNVHR8EXjBcMFqgWKBWhlRodHRwOi8vY2VydGVucm9sbC50ZXN0Lmdvc3VzbHVnaS5ydS9jZHAvYjBmZDhlYjk1OWQ5NDg5ZDViN2I0YzE0M2EwNmNhZDc5NTJhMDc0NC5jcmwwDAYFKoUDZHIEAwIBADCCAcMGA1UdIwSCAbowggG2gBSw/Y65WdlInVt7TBQ6BsrXlSoHRKGCAYmkggGFMIIBgTEVMBMGBSqFA2QEEgo3NzA3MDQ5Mzg4MRgwFgYFKoUDZAESDTEwMjc3MDAxOTg3NjcxCzAJBgNVBAYTAlJVMSkwJwYDVQQIDCA3OCDQodCw0L3QutGCLdCf0LXRgtC10YDQsdGD0YDQszEmMCQGA1UEBwwd0KHQsNC90LrRgi3Qn9C10YLQtdGA0LHRg9GA0LMxgZ4wgZsGA1UECQyBk9C80YPQvdC40YbQuNC/0LDQu9GM0L3Ri9C5INC+0LrRgNGD0LMg0KHQvNC+0LvRjNC90LjQvdGB0LrQvtC1INCS0J0u0KLQldCgLtCTLiwg0KHQuNC90L7Qv9GB0LrQsNGPINC90LDQsdC10YDQtdC20L3QsNGPLCDQtNC+0LwgMTQsINC70LjRgtC10YDQsCDQkDEmMCQGA1UECgwd0J/QkNCeICLQoNC+0YHRgtC10LvQtdC60L7QvCIxJTAjBgNVBAMMHNCi0LXRgdGC0L7QstGL0Lkg0KPQpiDQoNCi0JqCEQLRkKkAiLBYlkt8lE/Q3xYXMAoGCCqFAwcBAQMCA0EA2I4g60+gv4HfI/I3Mf9zQdAGQTAtQftInd+0QjNbXeKdtjbWhxVw9DAd8dhBSMo0zBCr/2G1vkZMqNeMooEkiQ==</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC8 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>169d856a-39b2-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>7e1c60e1-73eb-4ef0-ae0f-f364f7afb83a</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>1731fdfc-39b2-11f1-9205-b68311fca2ed</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiMTY5ZDg1NmEtMzliMi0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiN2UxYzYwZTEtNzNlYi00ZWYwLWFlMGYtZjM2NGY3YWZiODNhIiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJvcmlkIjpudWxsLCJyZW9sIjowfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<UpdateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<elkOrderNumber>0</elkOrderNumber>
									<orderNumber>1999880002</orderNumber>
									<status>28</status>
									<message>Order not found</message>
								</order>
							</orders>
						</UpdateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>1731fdfc-39b2-11f1-9205-b68311fca2ed</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T19:34:08.245+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T19:34:34.528+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>0JfV0dI0+O0sqZ63W+eKjDdDo7K2IxjiLC7Glblh/0U=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>C2hY4ps5TAGywZMNGULMv12KztSVqXuYUnxW0fIyxVnsGGCLfjF1EKg478w4Uk2oQL2Q50Fz0qINvQE26h1kwQ==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>MIII9DCCCKGgAwIBAgIRAu1s4gA3szG4SaWpjU5OezswCgYIKoUDBwEBAwIwggGBMRUwEwYFKoUDZAQSCjc3MDcwNDkzODgxGDAWBgUqhQNkARINMTAyNzcwMDE5ODc2NzELMAkGA1UEBhMCUlUxKTAnBgNVBAgMIDc4INCh0LDQvdC60YIt0J/QtdGC0LXRgNCx0YPRgNCzMSYwJAYDVQQHDB3QodCw0L3QutGCLdCf0LXRgtC10YDQsdGD0YDQszGBnjCBmwYDVQQJDIGT0LzRg9C90LjRhtC40L/QsNC70YzQvdGL0Lkg0L7QutGA0YPQsyDQodC80L7Qu9GM0L3QuNC90YHQutC+0LUg0JLQnS7QotCV0KAu0JMuLCDQodC40L3QvtC/0YHQutCw0Y8g0L3QsNCx0LXRgNC10LbQvdCw0Y8sINC00L7QvCAxNCwg0LvQuNGC0LXRgNCwINCQMSYwJAYDVQQKDB3Qn9CQ0J4gItCg0L7RgdGC0LXQu9C10LrQvtC8IjElMCMGA1UEAwwc0KLQtdGB0YLQvtCy0YvQuSDQo9CmINCg0KLQmjAeFw0yNTA4MTIxMzM0MjRaFw0yNjA4MTIxMzQ0MjRaMIIBvjEVMBMGBSqFA2QEEgo3NzEwNDc0Mzc1MRIwEAYJKoZIhvcNAQkCDANERVYxIDAeBgkqhkiG9w0BCQEWEXNkQHNjLm1pbnN2eWF6LnJ1MRgwFgYFKoUDZAESDTEwNDc3MDIwMjY3MDExGTAXBgNVBAoMENCc0LjQvdGG0LjRhNGA0YsxTTBLBgNVBAkMRNCf0YDQtdGB0L3QtdC90YHQutCw0Y8g0L3QsNCxLiwg0LQuIDEwLCDRgdGC0YAuIDIsIElRLdC60LLQsNGA0YLQsNC7MRUwEwYDVQQHDAzQnNC+0YHQutCy0LAxHDAaBgNVBAgMEzc3INCzLiDQnNC+0YHQutCy0LAxCzAJBgNVBAYTAlJVMYGoMIGlBgNVBAMMgZ3QnNC40L3QuNGB0YLQtdGA0YHRgtCy0L4g0YbQuNGE0YDQvtCy0L7Qs9C+INGA0LDQt9Cy0LjRgtC40Y8sINGB0LLRj9C30Lgg0Lgg0LzQsNGB0YHQvtCy0YvRhSDQutC+0LzQvNGD0L3QuNC60LDRhtC40Lkg0KDQvtGB0YHQuNC50YHQutC+0Lkg0KTQtdC00LXRgNCw0YbQuNC4MGYwHwYIKoUDBwEBAQEwEwYHKoUDAgIkAAYIKoUDBwEBAgIDQwAEQBhe7pMvFyU5u2cfvlZDP8p1uOBzFBA8w2MUwI3UJ8eS9hPbSV2pZmhkOlQit9NWHBYyO5EQYgZONaTwsQZZ3UyjggSqMIIEpjAOBgNVHQ8BAf8EBAMCA/gwHQYDVR0OBBYEFPsLxD95pbiL65oM7SOykYP2tx34MB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEFBQcDBDBUBggrBgEFBQcBAQRIMEYwRAYIKwYBBQUHMAKGOGh0dHA6Ly9jZXJ0ZW5yb2xsLnRlc3QuZ29zdXNsdWdpLnJ1L2NkcC90ZXN0X2NhX3J0azMuY2VyMB0GA1UdIAQWMBQwCAYGKoUDZHEBMAgGBiqFA2RxAjArBgNVHRAEJDAigA8yMDI1MDgxMjEzMzQyM1qBDzIwMjYwODEyMTMzNDIzWjCCATcGBSqFA2RwBIIBLDCCASgMMiLQmtGA0LjQv9GC0L7Qn9GA0L4gQ1NQIDQuMCBSNCIgKNCy0LXRgNGB0LjRjyA0LjApDCwi0JrRgNC40L/RgtC+0J/RgNC+INCj0KYiICjQstC10YDRgdC40LggMi4wKQxh0KHQtdGA0YLQuNGE0LjQutCw0YLRiyDRgdC+0L7RgtCy0LXRgtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDQodCkLzEyNC0zOTcxINC+0YIgMTUuMDEuMjAyMQxh0KHQtdGA0YLQuNGE0LjQutCw0YLRiyDRgdC+0L7RgtCy0LXRgtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDQodCkLzEyOC00Mzc2INC+0YIgMjguMTAuMjAyMjA9BgUqhQNkbwQ0DDIi0JrRgNC40L/RgtC+0J/RgNC+IENTUCA0LjAgUjQiICjQstC10YDRgdC40Y8gNC4wKTBlBgNVHR8EXjBcMFqgWKBWhlRodHRwOi8vY2VydGVucm9sbC50ZXN0Lmdvc3VzbHVnaS5ydS9jZHAvYjBmZDhlYjk1OWQ5NDg5ZDViN2I0YzE0M2EwNmNhZDc5NTJhMDc0NC5jcmwwDAYFKoUDZHIEAwIBADCCAcMGA1UdIwSCAbowggG2gBSw/Y65WdlInVt7TBQ6BsrXlSoHRKGCAYmkggGFMIIBgTEVMBMGBSqFA2QEEgo3NzA3MDQ5Mzg4MRgwFgYFKoUDZAESDTEwMjc3MDAxOTg3NjcxCzAJBgNVBAYTAlJVMSkwJwYDVQQIDCA3OCDQodCw0L3QutGCLdCf0LXRgtC10YDQsdGD0YDQszEmMCQGA1UEBwwd0KHQsNC90LrRgi3Qn9C10YLQtdGA0LHRg9GA0LMxgZ4wgZsGA1UECQyBk9C80YPQvdC40YbQuNC/0LDQu9GM0L3Ri9C5INC+0LrRgNGD0LMg0KHQvNC+0LvRjNC90LjQvdGB0LrQvtC1INCS0J0u0KLQldCgLtCTLiwg0KHQuNC90L7Qv9GB0LrQsNGPINC90LDQsdC10YDQtdC20L3QsNGPLCDQtNC+0LwgMTQsINC70LjRgtC10YDQsCDQkDEmMCQGA1UECgwd0J/QkNCeICLQoNC+0YHRgtC10LvQtdC60L7QvCIxJTAjBgNVBAMMHNCi0LXRgdGC0L7QstGL0Lkg0KPQpiDQoNCi0JqCEQLRkKkAiLBYlkt8lE/Q3xYXMAoGCCqFAwcBAQMCA0EAYHMbP9h8/c8bC89mLEeQ2rqvfELBas8rt+QYSy/Dy0w3AWqwXJ83myM8wwKqCHTJ2Z0MY7U66QlBY7NtxUAcjg==</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>KbKqnrr1Nown1aRl4P3OfrNLF48yk6lQ6rze8xzkuoc=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>tEZYljawdstLC2k5hRrnUxEpvqql6lgrMAYdoro2ANvd/bLXM55bE6fqRwjtsi/4RmCNwui+iIqwkz/PKEA8+w==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC9 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>36303149-3a62-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>3cc38404-d83d-40c1-8624-97a29257039a</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_ASYNC_BY_SMEV">
				<ns2:MessageID>36a058fd-3a62-11f1-b0d2-2712b17c77a0</ns2:MessageID>
				<ns2:To>eyJtaWQiOiIzNjMwMzE0OS0zYTYyLTExZjEtYjhiMi0wMjQyMzMzY2NlNTkiLCJ0Y2QiOiIzY2MzODQwNC1kODNkLTQwYzEtODYyNC05N2EyOTI1NzAzOWEiLCJzbGMiOiJ3cy5ydXB0by5ydV9zbWV2M19nb3N1c2x1Z2lfY2xpZW50c19tc3BfdG1fcmVnaXN0cmF0aW9uXzEuMC4wX1J1cHRvUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsImNydCI6IjIwMjYtMDQtMTdUMTY6MzQ6NTIuMjg4KzAzOjAwIiwibnMiOiJodHRwOi8vd3MucnVwdG8ucnUvc21ldjMvZ29zdXNsdWdpL2NsaWVudHMvbXNwL3RtX3JlZ2lzdHJhdGlvbi8xLjAuMCIsInNpZCI6MTkzODAxLCJvcmlkIjpudWxsLCJyZW9sIjowLCJlb2wiOjB9</ns2:To>
				<ns2:AsyncProcessingStatus>
					<ns2:OriginalMessageId>36303149-3a62-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
					<ns2:StatusCategory>responseIsRejectedBySmev</ns2:StatusCategory>
					<ns2:StatusDetails>Бизнес-данные сообщения не соответствуют схеме, зарегистрированной в СМЭВ. MessageId = 36303149-3a62-11f1-b8b2-0242333cce59</ns2:StatusDetails>
					<ns2:SmevFault xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns3:InvalidContent">
						<Code>028122</Code>
						<Description>SMEV-403: Бизнес-данные сообщения не соответствуют схеме, зарегистрированной в СМЭВ. MessageId = 36303149-3a62-11f1-b8b2-0242333cce59</Description>
						<ns3:ValidationError errorPosition="-1">cvc-complex-type.2.4.a: Invalid content was found starting with element '{"http://rupto.ru/standards/XMLSchema/epgu/1.0.1":changeOrderInfo}'. One of '{"http://rupto.ru/standards/XMLSchema/msp/1.0.0":changeOrderInfo, "http://rupto.ru/standards/XMLSchema/msp/1.0.0":cancelResponse}' is expected.</ns3:ValidationError>
					</ns2:SmevFault>
				</ns2:AsyncProcessingStatus>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>36a058fd-3a62-11f1-b0d2-2712b17c77a0</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>SMEV</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-17T16:34:52.288+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-17T16:35:33.703+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>ilXRaI81Q29Ak9D9pmN6/Q++GQ8GG4hIUPnl0xkLVH4=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>26Kgw9tughu1EXgJu+JSZNoIp0DjtlU9eYeVjsK/H2ZWPyMv7ihbk7mOftXqlupKNLHcmfwxAaptJ5/h7TqKqA==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC10 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>8335b169-395a-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>3977157b-3520-433b-99d2-c998c01aba87</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>846d47a1-395a-11f1-a6ab-b6df272c7906</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiODMzNWIxNjktMzk1YS0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiMzk3NzE1N2ItMzUyMC00MzNiLTk5ZDItYzk5OGMwMWFiYTg3IiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>11</code>
							<message>Completed with errors</message>
							<orders>
								<order>
									<orderNumber>1999880003</orderNumber>
									<status>38</status>
									<message>Request date too old</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>846d47a1-395a-11f1-a6ab-b6df272c7906</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T09:07:15.787+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T09:07:53.691+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>wdUxQkj1kZBvFtPgFscutXLmtr3YvvfhKVLL1eSJu3k=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>NXlw4/LA5/T8qu3i9ZeV13TGCD2VPOXK+E1+ZbeOkKIafxCp7MJuLrHN+sUZRo4WQXkyHsJ08auNNDZVmSPkiw==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>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</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>YFBre8BqD75W/4872QA7THod7uvXncvRU9UIwnia8oo=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>AAITwmJZSwYRAKYxXNw8rqjGw30LC0fadtZMBscb+lcYuUymB6TaMZ4V6fpDIHa+ulXe7/QGvKffua80XpWigA==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""

MC11 = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:GetResponseResponse xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:ns3="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/faults/1.2">
	<ns2:ResponseMessage>
		<ns2:Response Id="SIGNED_BY_SMEV">
			<ns2:OriginalMessageId>61e7a920-3968-11f1-b8b2-0242333cce59</ns2:OriginalMessageId>
			<ns2:OriginalTransactionCode>8d384e7d-a6a0-4cfd-918e-6616889ea7c5</ns2:OriginalTransactionCode>
			<ns2:SenderProvidedResponseData Id="SIGNED_BY_CALLER">
				<ns2:MessageID>8732c77a-3968-11f1-9205-b68311fca2ed</ns2:MessageID>
				<ns2:To>eyJzaWQiOjE5MzgwMSwibWlkIjoiNjFlN2E5MjAtMzk2OC0xMWYxLWI4YjItMDI0MjMzM2NjZTU5IiwidGNkIjoiOGQzODRlN2QtYTZhMC00Y2ZkLTkxOGUtNjYxNjg4OWVhN2M1IiwiZW9sIjowLCJzbGMiOiJlcGd1Lmdvc3VzbHVnaS5ydV9lbGtfc3RhdHVzXzEuMC4wX0Vsa09yZGVyUmVxdWVzdCIsIm1ubSI6IlJQVE4wMSIsIm5zIjoiaHR0cDovL2VwZ3UuZ29zdXNsdWdpLnJ1L2Vsay9zdGF0dXMvMS4wLjIiLCJyZW9sIjowLCJvcmlkIjpudWxsfQ==</ns2:To>
				<MessagePrimaryContent>
					<ElkOrderResponse:ElkOrderResponse xmlns:ElkOrderResponse="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns="http://epgu.gosuslugi.ru/elk/status/1.0.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
						<CreateOrdersResponse>
							<code>0</code>
							<message>OK</message>
							<orders>
								<order>
									<elkOrderNumber>4654266659</elkOrderNumber>
									<orderNumber>1999290001</orderNumber>
									<status>0</status>
									<message>OK</message>
								</order>
							</orders>
						</CreateOrdersResponse>
					</ElkOrderResponse:ElkOrderResponse>
				</MessagePrimaryContent>
			</ns2:SenderProvidedResponseData>
			<ns2:MessageMetadata>
				<ns2:MessageId>8732c77a-3968-11f1-9205-b68311fca2ed</ns2:MessageId>
				<ns2:MessageType>RESPONSE</ns2:MessageType>
				<ns2:Sender>
					<ns2:Mnemonic>MNSV05</ns2:Mnemonic>
				</ns2:Sender>
				<ns2:SendingTimestamp>2026-04-16T10:47:33.379+03:00</ns2:SendingTimestamp>
				<ns2:Recipient>
					<ns2:Mnemonic>RPTN01</ns2:Mnemonic>
				</ns2:Recipient>
				<ns2:DeliveryTimestamp>2026-04-16T10:47:34.384+03:00</ns2:DeliveryTimestamp>
				<ns2:Status>messageIsDelivered</ns2:Status>
			</ns2:MessageMetadata>
			<ns2:SenderInformationSystemSignature>
				<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2" xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
					<ds:SignedInfo>
						<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
						<ds:Reference URI="#SIGNED_BY_CALLER">
							<ds:Transforms>
								<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
								<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
							</ds:Transforms>
							<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
							<ds:DigestValue>wWcZql6UiLCOvDVCV6Ps1dILMkzZPRcGHvjIBWmVX60=</ds:DigestValue>
						</ds:Reference>
					</ds:SignedInfo>
					<ds:SignatureValue>0XCk4SBpTf91z6kM9f42irP4WHtPfaVFW6UzgYHVM0dNyYMxvSqq4g6fUTej9zXxdZvagQODvNpv6rWd4q5h6w==</ds:SignatureValue>
					<ds:KeyInfo>
						<ds:X509Data>
							<ds:X509Certificate>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</ds:X509Certificate>
						</ds:X509Data>
					</ds:KeyInfo>
				</ds:Signature>
			</ns2:SenderInformationSystemSignature>
		</ns2:Response>
		<ns2:SMEVSignature>
			<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
				<ds:SignedInfo>
					<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"/>
					<ds:Reference URI="#SIGNED_BY_SMEV">
						<ds:Transforms>
							<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
							<ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/>
						</ds:Transforms>
						<ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"/>
						<ds:DigestValue>rtRcLtZpYggZI+jOieH4guo36zvo4wYNbP4hgsRpOho=</ds:DigestValue>
					</ds:Reference>
				</ds:SignedInfo>
				<ds:SignatureValue>3WdkhSQ7TE0MSszuxvvK9PwOWFNY1oOFbZIJ1OsWDprCrV7s82yjWKQoscd6t5UCOh0qrXi/TQ5gODnrz2/fUw==</ds:SignatureValue>
				<ds:KeyInfo>
					<ds:X509Data>
						<ds:X509Certificate>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</ds:X509Certificate>
					</ds:X509Data>
				</ds:KeyInfo>
			</ds:Signature>
		</ns2:SMEVSignature>
	</ns2:ResponseMessage>
</ns2:GetResponseResponse>
"""
