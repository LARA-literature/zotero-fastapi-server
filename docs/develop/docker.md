# docker installation

## self signed certificate in certificate chain

cd docker/certs

openssl genrsa -out localhost-key.pem 2048
openssl req -new -key localhost-key.pem -out localhost.csr
openssl x509 -req -days 365 -in localhost.csr -signkey localhost-key.pem -out localhost-cert.pem


# signature output
openssl x509 -req -days 365 -in localhost.csr -signkey localhost-key.pem -out localhost-cert.pem
Certificate request self-signature ok
subject=C=DE, ST=Some-State, L=Greifswald, O=UG, OU=UG, CN=zotero-fastapi-server, emailAddress=mark.doerr@uni-greifsald.de