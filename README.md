First Steps
-----------

## Setup swagger codegen tools via Docker
- added `~/.zshrc` alias for [Swagger Codegen CLI tool](https://github.com/swagger-api/swagger-codegen#public-pre-built-docker-images)

Code Generation
---------------
General help `swagger-gen generate help`
For Flask generation specific options go for `swagger-gen config-help -l python-flask`
swagger-gen --api-package api_pack -i eark-validation.yaml --invoker-package inv_pack -l python-rest --model-package model_pack -o gentest -v
