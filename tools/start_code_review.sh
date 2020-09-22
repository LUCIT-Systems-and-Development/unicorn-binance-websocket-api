#!/bin/env bash

curl -X POST --data-binary @patch-file.bin \
'https://lgtm.com/api/v1.0/codereviews/1512645096514?base=047b10a49ce9d277d35f140aebde333f36e14b6c&external-id=14794' \
  -H 'Content-Type: application/octet-stream' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer 086ddbf968c84b9efb91f90d0b4f95a23bc9804fc1a416a4e2daca3e9570f498'