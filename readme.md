# 概要

S3に保存されたSwaggerファイルから各種開発者向け資産の配布を行うためのマイクロサービス。

SetupFunctionsで繋ぐ想定。

# 必要なもの

* Swagger CodeGenerator(WebServiceとして利用)
* Swagger UI

# 入力

## distribute_client

```
{
  "swaggerUrl": "string", # Swaggerファイルのurl
  "language": "string", # 各言語の指定(e.g. java,javascript, ruby, scala...)
  "serviceName": "string" # 出力するサービス名
}
```

`ベースのバケット/サービス名/言語名/言語名-generated-client.zip` で出力される。
