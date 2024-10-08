# -*- coding: utf-8 -*-
"""Trabalho_Final_[Big_Data].ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VulR3GznC8uENLW2yoGOxTeL5Kb83h3I

# Pipeline de Limpeza e Transformação para Aplicações de IA com PySpark SQL

Grupo:
- Regis Lukas
- Pedro Armando
- Júlia Rodrigues
- Yasmin Helena
- Beatriz Vencio
"""

# Instalação do PySpark
!pip install pyspark

# Importação das bibliotecas necessárias
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, avg, sum, count, mean
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler

# Criação de uma sessão Spark
spark = SparkSession.builder.appName("IA_Pipeline").getOrCreate()

# Define o esquema dos dados
schema = StructType([
    StructField("User_ID", IntegerType(), True),
    StructField("Product_ID", StringType(), True),
    StructField("Gender", StringType(), True),
    StructField("Age", StringType(), True),
    StructField("Occupation", IntegerType(), True),
    StructField("City_Category", StringType(), True),
    StructField("StayInCurrentCityYears", StringType(), True),
    StructField("Marital_Status", IntegerType(), True),
    StructField("ProductCategory", IntegerType(), True),
    StructField("Purchase", IntegerType(), True)
])

# Carrega os dados brutos do CSV
data = spark.read.format("csv") \
  .option("header", "true") \
  .schema(schema) \
  .load("/content/walmart.csv")

"""Limpeza de dados"""

# nesse exemplo, não há necessidade de limpar dados faltantes

# Transformações
data = data.withColumn("Age_Group", when(col("Age") == "0-17", "Menor de 18") \
                            .when(col("Age") == "18-25", "Jovem Adulto") \
                            .when(col("Age") == "26-35", "Adulto") \
                            .when(col("Age") == "36-45", "Meia Idade") \
                            .when(col("Age") == "46-50", "Pré-aposentadoria") \
                            .when(col("Age") == "51-55", "Pré-aposentadoria") \
                            .otherwise("Aposentado")) # Cria uma nova coluna com grupos de idade

# Agregações
data_agregada = data.groupBy("City_Category") \
  .agg(avg("Purchase").alias("Purchase_Average"), count("*").alias("Number_of_Purchases"))

"""Preparação para Machine Learning"""

# Codificação de variáveis categóricas
indexer = StringIndexer(inputCol="Gender", outputCol="Gender_Index")
model = indexer.fit(data)
data = model.transform(data)

encoder = OneHotEncoder(inputCol="Gender_Index", outputCol="Gender_Vec")
encoderModel = encoder.fit(data) # Treina o modelo
data = encoderModel.transform(data) # Aplica a transformação

# Codificação de variáveis categóricas
indexer = StringIndexer(inputCol="Age", outputCol="Age_Index")
model = indexer.fit(data)
data = model.transform(data)

encoder = OneHotEncoder(inputCol="Age_Index", outputCol="Age_Vec")
encoderModel = encoder.fit(data) # Treina o modelo
data = encoderModel.transform(data) # Aplica a transformação

# Codificação de variáveis categóricas
indexer = StringIndexer(inputCol="City_Category", outputCol="City_Category_Index")
model = indexer.fit(data)
data = model.transform(data)

encoder = OneHotEncoder(inputCol="City_Category_Index", outputCol="City_Category_Vec")
encoderModel = encoder.fit(data) # Treina o modelo
data = encoderModel.transform(data) # Aplica a transformação

# Codificação de variáveis categóricas
indexer = StringIndexer(inputCol="StayInCurrentCityYears", outputCol="StayInCurrentCityYears_Index")
model = indexer.fit(data)
data = model.transform(data)

encoder = OneHotEncoder(inputCol="StayInCurrentCityYears_Index", outputCol="StayInCurrentCityYears_Vec")
encoderModel = encoder.fit(data) # Treina o modelo
data = encoderModel.transform(data) # Aplica a transformação

# Criação do vetor de features
assembler = VectorAssembler(inputCols=["Age_Vec", "Occupation", "City_Category_Vec", "StayInCurrentCityYears_Vec", "Marital_Status", "ProductCategory", "Gender_Vec"], outputCol="features")
data = assembler.transform(data)

# Exporta os dados limpos e transformados
data.write.format("parquet").save("path/to/your/processed_data")

# Imprime os resultados
data_agregada.show()