Curl Examples
-------------
You need a SHA1 checksum to upload a file. This ensures that the file isn't altered
in transmission, so calculate first.
```
$ sha1sum minimal_IP_invmets.zip
6e68f1130f7970435a2e61934e9dd942ae8562bd  minimal_IP_invmets.zip
```
If you POST a package with a bad digest you'll see something like this:
```
curl -F "package=@minimal_IP_invmets.zip" -F "digest=6e68f1130f7970435a2e61934e9dd942ae8562dd" http://localhost:5000/api/ip/package/
{"message":"Digest mismatch, calculated 8cdc4eadc217f952fcea769423289a5326aa893b, POSTED 6e68f1130f7970435a2e61934e9dd942ae8562dd"}
```
Now POST the package file and it's digest as form encoded data to the package
upload URL, you'll get confirmation of the digest and a URL from which to collect
the validation results.
```
$ curl -F "package=@minimal_IP_invmets.zip" -F "digest=6e68f1130f7970435a2e61934e9dd942ae8562bd" http://localhost:5000/api/ip/package/
{"sha1":"6e68f1130f7970435a2e61934e9dd942ae8562bd","validation_url":"http://localhost:5050/api/ip/validate/6e68f1130f7970435a2e61934e9dd942ae8562bd/"}
```
Now a simple GET at the validation URL to get the JSON results, this one has warnings:
```
$ curl http://localhost:5000/api/ip/validation/6e68f1130f7970435a2e61934e9dd942ae8562bd/
{
  "metadata_valid":false,
  "profile_warnings":[
    {
      "location":"/*[local-name()='mets' and namespace-uri()='http://www.loc.gov/METS/']",
      "message":"Must be used if descriptive metadata about the package content is available. NOTE: According to official METS documentation each metadata section must describe one and only one set of metadata. As such, if implementers want to include multiple occurrences of descriptive metadata into the package this must be done by repeating the whole dmdSec element for each individual metadata.",
      "rule_id":"CSIP17",
      "severity":"Warn",
      "test":"mets:dmdSec"
    },
    {
      "location":"/*[local-name()='mets' and namespace-uri()='http://www.loc.gov/METS/']",
      "message":"If administrative / preservation metadata is available, it must be described using the administrative metadata section (amdSec) element. All administrative metadata is present in a single amdSec element.",
      "rule_id":"CSIP31",
      "severity":"Warn",
      "test":"mets:amdSec"
    },
    {
      "location":"/*[local-name()='mets' and namespace-uri()='http://www.loc.gov/METS/']/*[local-name()='metsHdr' and namespace-uri()='http://www.loc.gov/METS/']",
      "message":"The metsHdr element SHOULD have a LASTMODDATE attribute.",
      "rule_id":"CSIP8",
      "severity":"Warn",
      "test":"@LASTMODDATE"
    }
  ],
  "schema_errors":[],
  "schema_valid":true
}
```
This one fails METS schema validation:
```
$ curl http://localhost:5000/api/ip/validation/8cdc4eadc217f952fcea769423289a5326aa893b/
{
  "metadata_valid":null,
  "profile_warnings":[],
  "schema_errors":["Element '{http://www.loc.gov/METS/}namez': This element is not expected. Expected is ( {http://www.loc.gov/METS/}name )."],
  "schema_valid":false}
```
