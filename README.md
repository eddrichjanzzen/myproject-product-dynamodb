


# Setup Dynamodb Backend

## Prerequisites
- Must have a working implementation of Backend Python Flask RestAPI
- Link: [https://github.com/ejanzzenang/myproject-product-restapi](https://github.com/ejanzzenang/myproject-product-restapi)

- docker-compose
```
$ docker-compose -v
docker-compose version 1.23.2, build 1110ad01
```

## Directory Structure
Your current directory structure from the previous module must look like this:
```
~/environment/myproject-product-restapi
├── README.md
└── product-management
    ├── Dockerfile
    ├── api
    │   ├── app.py
    │   ├── custom_logger.py
    │   └── products
    │       └── product_routes.py
    └── requirements.txt
```
*Note that we will be building on top of `myproject-product-restapi`
## Step 1: Add Data tier with DynamoDB

### Step 1.1: Prepare DynamoDB Table Schema
Create file `product-schema.json` in `aws-cli` folder
```
$ cd ~/environment/python-restapi-service
$ mkdir aws-cli
$ cd aws-cli
$ touch product-schema.json
```
```json
{
  "TableName": "ProductTable",
  "ProvisionedThroughput": {
    "ReadCapacityUnits": 5,
    "WriteCapacityUnits": 5
  },
  "AttributeDefinitions": [
    {
      "AttributeName": "id",
      "AttributeType": "S"
    },
    {
      "AttributeName": "name",
      "AttributeType": "S"
    }
  ],
  "KeySchema": [
    {
      "AttributeName": "id",
      "KeyType": "HASH"
    }
  ],
  "GlobalSecondaryIndexes": [
    {
      "IndexName": "name_index",
      "KeySchema": [
        {
          "AttributeName": "name",
          "KeyType": "HASH"
        },
        {
          "AttributeName": "id",
          "KeyType": "RANGE"
        }
      ],
      "Projection": {
        "ProjectionType": "ALL"
      },
      "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
      }
    }
  ]
}
```

### Step 1.2: Run Dynamodb Local Instance
 In `product-management` folder, create the following file `docker-compose.yaml`

```
$ cd product-management
$ touch docker-compose.yaml
```
```docker
version: '3'
services:
  # This creates a local version of dynamodb
  # https://github.com/aws-samples/aws-sam-java-rest/issues/1
  dynamo-db:
    image: amazon/dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - dynamodb_data:/home/dynamodblocal
    working_dir: /home/dynamodblocal
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ."
  
  # backend api service
  api:
    build: .
    volumes:
      - .:/code
    ports:
      - '8080:8080'
    links: 
      - dynamo-db
    working_dir: /code/api
volumes:
  dynamodb_data:
```

### Step 1.3:  Create a DynamoDB Table
In a new terminal: run the following command:
```
 aws dynamodb create-table \
--cli-input-json file://~/environment/myproject-product-restapi/product-schema.json \
--endpoint-url http://localhost:8000
```

### Step 1.4:  Prepare Items to upload
Create file `populate-product.json` in `aws-cli` folder
```json
{
      "ProductTable" : [
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"4d196c50-aabf-4df2-afb3-fd21481259d6"
                  },
                  "name":{
                     "S":"Boracay Sunset Cruise"
                  },
                  "description":{
                     "S":"The Boracay sunset is a spectacular site to see and what better way than cruising on the ocean with an icy cold beverage!  Tour along White Beach and take in all the tropical sights and sounds while you enjoy the spectacular arrays of color of the Boracay sunset.  Stop off for a quick swim, stand up paddle and snorkel or chill out in tube before heading back to enjoy your dinner in paradise."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2019/02/Boracay-Sunset-Cruise-00-400x267.jpg"
                  },
                  "price":{
                     "N":"800"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"6b3c211a-53f3-4c2a-a4f3-dc1fd5d42bfc"
                  },
                  "name":{
                     "S":"Group Island Hopping"
                  },
                  "description":{
                     "S":"Make new friends by joining a shared boat cruise where you will cruise the shores of Boracay in a traditional Banka boat. Visit the famous Puka shell beach and take a stroll on the beach, swim in the azure waters or just relax with a fresh coconut enjoying the sun. Stop off for a snorkel and see Boracay\u2019s beautiful tropical fish and corals.  Finish the trip with a delicious buffet lunch."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2019/03/Boracay-Group-Island-Hopping-Boracay-Activities-01-400x267.jpg"
                  },
                  "price":{
                     "N":"1500"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"91e759dc-f385-42e1-8098-a44399bebce8"
                  },
                  "name":{
                     "S":"Ultimate Cliff Jumping Island Hopping Adventure"
                  },
                  "description":{
                     "S":"Experience a day of fun on Magic Island and have the thrill of a lifetime with 5 different levels of cliff jumping. Relax and swim or go snorkeling around the Island."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/06/Island-Hopping-Boracay-Activities-400x267-400x267.jpg"
                  },
                  "price":{
                     "N":"2200"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"2178bb44-32f1-4d22-bc95-05cd039a3067"
                  },
                  "name":{
                     "S":"4 Hour Private Boracay Island Hopping Package"
                  },
                  "description":{
                     "S":"Your Boracay adventure experience will not be complete without this trip! The island is home to more than a dozen undeveloped beaches, turquoise waters and colorful coral reefs! Feast your eyes on the amazing scenery, snorkel and get a glimpse of the thriving sea life!The boat trip includes stopover at some amazing places in Boracay where you can go snorkeling and swimming. Snorkeling gears will be provided for you."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/09/Private-Island-Hopping-Boracay-Activity-8-400x267.jpg"
                  },
                  "price":{
                     "N":"2900"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"8f086c95-df7d-4914-98b5-e3378663e967"
                  },
                  "name":{
                     "S":"Paraw Sailing"
                  },
                  "description":{
                     "S":"Paraw Sailing is a local sail boat\u00a0activity. The boats use two outriggers and two sails. Experience the traditional way of sailing and discover the best sites around the island, perfect for photography \u2013 though do note on days with heavier waves the water can kick up a bit (exciting!). If you schedule your activity for later in the afternoon you can take advantage of the incredible sunset while relaxing on the boat for half an hour. Sea sickness? usually not a problem as the boats tend to stay closer into the shore and cut through the waves very well. \u00a0Paraw sailing around Boracay is probably a really good way to ease yourself into the sea and find out how much you like it."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/03/Paraw-Sailing-Boracay-Activities-400x267.jpg"
                  },
                  "price":{
                     "N":"3000"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"6aa0ed0f-ddcc-42ff-8059-eea5ee40496d"
                  },
                  "name":{
                     "S":"Parasailing"
                  },
                  "description":{
                     "S":"Parasailing on Boracay is a great experience for a few adventure-minded individuals. Imagine being whisked into the sky while strapped in a seat covered by a colorful parachute! This is a popular activity where riders can view the beautiful shoreline of white beach from above while being pulled by a boat. This is a fun and exciting experience for those who love heights and want a birds-eye-view of the whole island. Up to two guests can occupy the same canopy."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/04/Parasailing-Boracay-Activities-400x267.jpg"
                  },
                  "price":{
                     "N":"2500"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"c5f7878a-70cd-49da-9a24-ca0b86beb71c"
                  },
                  "name":{
                     "S":"Boracay Pub Crawl"
                  },
                  "description":{
                     "S":"Boracay Pub Crawl is the biggest, hippest and most happening bar-hopping event on Boracay! Meet amazing people from around the world, play get to know you games to break the ice, drink welcome shooters with your free shooter glass, get discounts on drinks, free entrance in bars, and wear your iconic pub crawl shirt! This is definitely one of the most awesome ways to experience the island\u2019s famous nightlife and also a great chance to take pictures. Boracay PubCrawl is the first of its kind to offer both travelers and locals the chance to party as one big, wild group. Discover the best night spots and make new friends over the course of a great evening out."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/04/Boracay-Pub-Crawl-Activities-400x267.jpeg"
                  },
                  "price":{
                     "N":"990"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"0c3b6e63-9a92-4662-8a44-d3d9adc334c2"
                  },
                  "name":{
                     "S":"Sunset Party Cruise Booty"
                  },
                  "description":{
                     "S":"Aside from its amazing parties, Boracay is world famous for its breath-taking sunset. Hop on the island\u2019s 40 passenger party vessel, Booty, and jam with other travelers as you listen to great music! Definitely a memorable party at sundown!"
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/04/Sunset-Party-Cruise-Booty-400x267.jpg"
                  },
                  "price":{
                     "N":"2500"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"36b74f58-084d-4b67-9daa-a046296604e6"
                  },
                  "name":{
                     "S":"Ariels Point"
                  },
                  "description":{
                     "S":"Let us help you experience everything good about Ariel\u2019s Point. Many guests come for the 5 different levels of cliff diving; the cliff diving levels are generally suitable for all types of adventurers. Those that want a great photo in a naturally beautiful place\u00a0while having a bit of a jump, won\u2019t be disappointed or terrified. Similarly, hardcore guests that want to jump from the top of a volcanically hewn outcrop into the deep blue arms of the sea won\u2019t be let down either. \u00a0Ariel\u2019s Point is located near the rustic fishing town of Buruanga, a half hour boat ride from Boracay\u2019s white beach. Gather with other travelers as you snorkel, paddle in a native canoe, or just laze under the sun while enjoying the uniquely rough, &\u00a0comfortable environment."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/04/Ariels-Point-Boracay-Activities-1-400x267.jpg"
                  },
                  "price":{
                     "N":"2800"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"420cb55b-99cb-45b1-a860-d079cc1d2cea"
                  },
                  "name":{
                     "S":"Stand Up Paddle on the Beach"
                  },
                  "description":{
                     "S":"Experience how it\u2019s like to glide on the water surface from a Stand-Up Paddle Board. Paddling on a Stand-Up Paddle board for lets you commune with the current of the sea, either by standing up, kneeling or sitting down. It also provides a good exercise to maintain your balance and to strengthen your core, while you paddle into the water to workout your arms and upper body."
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/10/Stand-Up-Paddle-Boracay-Activity-01-400x267.jpg"
                  },
                  "price":{
                     "N":"1000"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"778bad3e-6fb4-4deb-8ff2-120bcbc5f27e"
                  },
                  "name":{
                     "S":"Segway Tours"
                  },
                  "description":{
                     "S":"Surrender to the freedom of gliding along Boracay\u2019s scenic spots on a Segway. For an exhilarating hour, you will be able to feel a gratifying oneness with the Segway and surrender to its awesome mechanism, giving you a relaxed and confident exploration into the island\u2019s diverse sceneries. This eco-freindly joyride kicks off with a short video presentation at its booth inside the panoramic grounds of Fairways and Blue Water. A routine trial thence follows, and after, the actual Segway ride takes place. The first leg encompasses a comfortable descent on the pavement, where beginners"
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2016/08/Segway-Tours-Boracay-Activities-01-400x267.jpg"
                  },
                  "price":{
                     "N":"2300"
                  }
               }
            }
         },
         {
            "PutRequest":{
               "Item":{
                  "id":{
                     "S":"7c72e357-7228-4b6c-bdd0-d9aab71512ac"
                  },
                  "name":{
                     "S":"Helicopter Beach Tour"
                  },
                  "description":{
                     "S":"Boracay Helicopter Beach Tour \u2013 It\u2019s never been better. Have a 10-minute adrenaline-filled experience of touring the island by helicopter! See Boracay\u2019s white sands, blue green waters, and reefs from above! This is the ultimate chance to snap birds-eye-view photographs!"
                  },
                  "image_url":{
                     "S":"https://cdn5.myboracayguide.com/2010/01/Boracay-Helicopter-Tours-Boracay-Activity-07-400x267.jpg"
                  },
                  "price":{
                     "N":"5200"
                  }
               }
            }
         }
      ]
   }
```
### Step 1.3:  Add Items to the DynamoDB Table
Run the following commands in order
```bash
$ aws dynamodb batch-write-item --request-items file://~/enviroment/myproject-product-restapi/aws-cli/populate-product.json --endpoint-url http://localhost:8000

# Use to scan existing tables
$ aws dynamodb scan --table-name ProductTable --endpoint-url http://localhost:8000
```

### Step 1.5: Setup .env file

In `api/` folder, create the following file:  `.env`
```
$ cd api
$ touch .env
```
```
DYNAMODB_ENDPOINT_URL=http://dynamo-db:8000/
TABLE_NAME=ProductTable
```

### Step 1.6:  Create Client to Interact with Dynamodb

In `api/products/` folder, create the following file:   `product_table_client.py`

```
$ cd api/products
$ touch product_table_client.py
```
 
```python
import boto3
import json
import logging
from collections import defaultdict
import argparse
from decouple import config
import uuid
from custom_logger import setup_logger

logger = setup_logger(__name__)

# For production: 

# create a DynamoDB client using boto3. The boto3 library will automatically
# use the credentials associated with our ECS task role to communicate with
# DynamoDB, so no credentials need to be stored/managed at all by our code!

# For local development
# we need to specify the aws access keys to be random string

dynamodb = boto3.client('dynamodb', 
            endpoint_url=config('DYNAMODB_ENDPOINT_URL', default='http://dynamo-db:8000/'),
            region_name=config('REGION', default='ap-southeast-1'),
            aws_access_key_id='x',
            aws_secret_access_key='x'
             )

table_name = config('TABLE_NAME', default='SampleTable')


# dynamodb = boto3.client('dynamodb')
# table_name = 'ProductTable'

def getJsonData(items):
    # create a default dictonary
    product_list = defaultdict(list)
    
    # loop through the items given as parameters
    for item in items:
    # define product payload object
        product = {
            'id': item["id"]["S"],
            'name': item['name']['S'],
            'description': item['description']['S'],
            'image_url': item['image_url']['S'],
            'price': item['price']['N'],
        }
        product_list['products'].append(product)

    return product_list
    
def getAllProducts():

    response = dynamodb.scan(
        TableName=table_name
    )
        
    # loop through the returned dict and convert this into json
    data_list = getJsonData(response["Items"])
    
    return json.dumps(data_list)

# Retrive a single mysfit from DynamoDB using their unique mysfitId
def getProduct(product_id):

    # get a product by its unique key
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        }
    )


    # check if the item exists in dynamodb
    if 'Item' in response:
        item = response['Item']

        logger.info("Get Product Response: ")
        logger.info(response)
        
        # define product payload object
        product = {
            'id': item["id"]["S"],
            'name': item['name']['S'],
            'description': item['description']['S'],
            'image_url': item['image_url']['S'],
            'price': item['price']['N'],
        }

    else:

        product = {
            'status' : "The product with id: {} does not exist.".format(product_id)
        }


    return json.dumps(product)

def createProduct(product_dict):

    product_id = str(uuid.uuid4())
    product_name = str(product_dict['name'])
    product_description = str(product_dict['description'])
    product_image_url = str(product_dict['image_url'])
    price = str(product_dict['price'])


    response = dynamodb.put_item(
        TableName=table_name,
        Item={
                'id': {
                    'S': product_id
                },
                'name': {
                    'S' : product_name
                },
                'description' : {
                    'S' : product_description
                },
                'image_url': {
                    'S' : product_image_url
                },
                'price': {
                    'N' : price
                }             
            }
        )

    # define product payload object

    product = {
        'id': item["id"]["S"],
        'name': item['name']['S'],
        'description': item['description']['S'],
        'image_url': item['image_url']['S'],
        'price': item['price']['N'],
        'status' : 'CREATED OK'
    }

    return json.dumps(product)

def updateProduct(product_id, product_dict):

    # example used for updating values
    # https://stackoverflow.com/questions/37721245/boto3-updating-multiple-values
    name = str(product_dict['name'])
    description = str(product_dict['description'])
    image_url = str(product_dict['image_url'])
    price = str(product_dict['price'])

    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        },
        UpdateExpression="""SET name = :p_name, 
                                description = :p_description,
                                image_url = :p_image_url,
                                price = :p_price
                                """,
        ExpressionAttributeValues={
            ':p_name': {
                'S' : product_name
            },
            ':p_description' : {
                'S' : product_description
            },
            ':p_image_url': {
                'S' : image_url
            },
            ':p_image_url': {
                'N' : price
            }              
        }
    )


    logger.info("Update Product Response: ")
    logger.info(response)

    # define product payload object
    product = {
        'id': item["id"]["S"],
        'name': item['name']['S'],
        'description': item['description']['S'],
        'image_url': item['image_url']['S'],
        'price': item['price']['N'],
        'status' : 'UPDATED OK'
    }


    return json.dumps(product)

def deleteProduct(product_id):

    response = dynamodb.delete_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        }
    )

    product = {
        'id' : product_id,
        'status' : 'DELETED OK'
    }

    return json.dumps(product)
```

### Step 1.7: Modify Routes to consume data from our Dynamodb Client
In `api/products/` folder, modify the following file:   `product_table_client.py`

```python
import boto3
import json
import logging
from collections import defaultdict
import argparse
from decouple import config
import uuid
from custom_logger import setup_logger


logger = setup_logger(__name__)

# For production: 

# create a DynamoDB client using boto3. The boto3 library will automatically
# use the credentials associated with our ECS task role to communicate with
# DynamoDB, so no credentials need to be stored/managed at all by our code!

# For local development
# we need to specify the aws access keys to be random string

dynamodb = boto3.client('dynamodb', 
            endpoint_url=config('DYNAMODB_ENDPOINT_URL', default='http://dynamo-db:8000/'),
            region_name=config('REGION', default='ap-southeast-1'),
            aws_access_key_id='x',
            aws_secret_access_key='x'
        )

table_name = config('TABLE_NAME', default='SampleTable')


# dynamodb = boto3.client('dynamodb')
# table_name = 'ProductTable'

def getJsonData(items):
    # create a default dictonary
    product_list = defaultdict(list)
    
    # loop through the items given as parameters
    for item in items:
    # define product payload object
        product = {
            'id': item["id"]["S"],
            'name': item['name']['S'],
            'description': item['description']['S'],
            'image_url': item['image_url']['S'],
            'price': item['price']['N'],
        }
        product_list['products'].append(product)

    return product_list
    
def getAllProducts():

    response = dynamodb.scan(
        TableName=table_name
    )
        
    # loop through the returned dict and convert this into json
    data_list = getJsonData(response["Items"])
    
    return json.dumps(data_list)

# Retrive a single mysfit from DynamoDB using their unique mysfitId
def getProduct(product_id):

    # get a product by its unique key
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        }
    )


    # check if the item exists in dynamodb
    if 'Item' in response:
        item = response['Item']

        logger.info("Get Product Response: ")
        logger.info(response)
        
        # define product payload object
        product = {
            'id': item["id"]["S"],
            'name': item['name']['S'],
            'description': item['description']['S'],
            'image_url': item['image_url']['S'],
            'price': item['price']['N'],
        }

    else:

        product = {
            'status' : "The product with id: {} does not exist.".format(product_id)
        }


    return json.dumps(product)

def createProduct(product_dict):

    product_id = str(uuid.uuid4())
    name = str(product_dict['name'])
    description = str(product_dict['description'])
    image_url = str(product_dict['image_url'])
    price = str(product_dict['price'])


    response = dynamodb.put_item(
        TableName=table_name,
        Item={
                'id': {
                    'S': product_id
                },
                'name': {
                    'S' : name
                },
                'description' : {
                    'S' : description
                },
                'image_url': {
                    'S' : image_url
                },
                'price': {
                    'N' : price
                }             
            }
        )


    # define product payload object

    product = {
        'id': product_id,
        'name': name,
        'description': description,
        'image_url': image_url,
        'price': price,
        'status' : 'CREATED OK'
    }

    return json.dumps(product)

def updateProduct(product_id, product_dict):

    # TODO: Fix validation for record updates

    # example used for updating values
    # https://stackoverflow.com/questions/37721245/boto3-updating-multiple-values
    product_name = str(product_dict['name'])
    description = str(product_dict['description'])
    image_url = str(product_dict['image_url'])
    price = str(product_dict['price'])

    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        },
        UpdateExpression="""SET product_name = :p_name, 
                                description = :p_description,
                                image_url = :p_image_url,
                                price = :p_price
                                """,
        ExpressionAttributeValues={
            ':p_name': {
                'S' : product_name
            },
            ':p_description' : {
                'S' : description
            },
            ':p_image_url': {
                'S' : image_url
            },
            ':p_price': {
                'N' : price
            }              
        }
    )


    logger.info("Update Product Response: ")
    logger.info(response)

    # define product payload object
    product = {
        'name': product_name,
        'description': description,
        'image_url': image_url,
        'price': price,
        'status' : 'UPDATED OK'
    }


    return json.dumps(product)

def deleteProduct(product_id):

    response = dynamodb.delete_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        }
    )

    product = {
        'id' : product_id,
        'status' : 'DELETED OK'
    }

    return json.dumps(product)

```

### Step 1.8: Restart Application and Dynamodb Local

```
$ docker-compose down
$ docker-compose up
```

### Step 1.14: Test CRUD Operations
- Test Get all Products
```
curl -X GET \
  http://localhost:8080/products \
  -H 'Host: localhost:8080'
```
```
{
    "products": [
        {
            "id": "7c72e357-7228-4b6c-bdd0-d9aab71512ac",
            "name": "Helicopter Beach Tour",
            "description": "Boracay Helicopter Beach Tour – It’s never been better. Have a 10-minute adrenaline-filled experience of touring the island by helicopter! See Boracay’s white sands, blue green waters, and reefs from above! This is the ultimate chance to snap birds-eye-view photographs!",
            "image_url": "https://cdn5.myboracayguide.com/2010/01/Boracay-Helicopter-Tours-Boracay-Activity-07-400x267.jpg",
            "price": "5200"
        },
        {
            "id": "36b74f58-084d-4b67-9daa-a046296604e6",
            "name": "Ariels Point",
            "description": "Let us help you experience everything good about Ariel’s Point. Many guests come for the 5 different levels of cliff diving; the cliff diving levels are generally suitable for all types of adventurers. Those that want a great photo in a naturally beautiful place while having a bit of a jump, won’t be disappointed or terrified. Similarly, hardcore guests that want to jump from the top of a volcanically hewn outcrop into the deep blue arms of the sea won’t be let down either.  Ariel’s Point is located near the rustic fishing town of Buruanga, a half hour boat ride from Boracay’s white beach. Gather with other travelers as you snorkel, paddle in a native canoe, or just laze under the sun while enjoying the uniquely rough, & comfortable environment.",
            "image_url": "https://cdn5.myboracayguide.com/2016/04/Ariels-Point-Boracay-Activities-1-400x267.jpg",
            "price": "2800"
        },
        {
            "id": "420cb55b-99cb-45b1-a860-d079cc1d2cea",
            "name": "Stand Up Paddle on the Beach",
            "description": "Experience how it’s like to glide on the water surface from a Stand-Up Paddle Board. Paddling on a Stand-Up Paddle board for lets you commune with the current of the sea, either by standing up, kneeling or sitting down. It also provides a good exercise to maintain your balance and to strengthen your core, while you paddle into the water to workout your arms and upper body.",
            "image_url": "https://cdn5.myboracayguide.com/2016/10/Stand-Up-Paddle-Boracay-Activity-01-400x267.jpg",
            "price": "1000"
        },
        {
            "id": "6aa0ed0f-ddcc-42ff-8059-eea5ee40496d",
            "name": "Parasailing",
            "description": "Parasailing on Boracay is a great experience for a few adventure-minded individuals. Imagine being whisked into the sky while strapped in a seat covered by a colorful parachute! This is a popular activity where riders can view the beautiful shoreline of white beach from above while being pulled by a boat. This is a fun and exciting experience for those who love heights and want a birds-eye-view of the whole island. Up to two guests can occupy the same canopy.",
            "image_url": "https://cdn5.myboracayguide.com/2016/04/Parasailing-Boracay-Activities-400x267.jpg",
            "price": "2500"
        },
        {
            "id": "6b3c211a-53f3-4c2a-a4f3-dc1fd5d42bfc",
            "name": "Group Island Hopping",
            "description": "Make new friends by joining a shared boat cruise where you will cruise the shores of Boracay in a traditional Banka boat. Visit the famous Puka shell beach and take a stroll on the beach, swim in the azure waters or just relax with a fresh coconut enjoying the sun. Stop off for a snorkel and see Boracay’s beautiful tropical fish and corals.  Finish the trip with a delicious buffet lunch.",
            "image_url": "https://cdn5.myboracayguide.com/2019/03/Boracay-Group-Island-Hopping-Boracay-Activities-01-400x267.jpg",
            "price": "1500"
        },
        {
            "id": "91e759dc-f385-42e1-8098-a44399bebce8",
            "name": "Ultimate Cliff Jumping Island Hopping Adventure",
            "description": "Experience a day of fun on Magic Island and have the thrill of a lifetime with 5 different levels of cliff jumping. Relax and swim or go snorkeling around the Island.",
            "image_url": "https://cdn5.myboracayguide.com/2016/06/Island-Hopping-Boracay-Activities-400x267-400x267.jpg",
            "price": "2200"
        },
        {
            "id": "8f086c95-df7d-4914-98b5-e3378663e967",
            "name": "Paraw Sailing",
            "description": "Paraw Sailing is a local sail boat activity. The boats use two outriggers and two sails. Experience the traditional way of sailing and discover the best sites around the island, perfect for photography – though do note on days with heavier waves the water can kick up a bit (exciting!). If you schedule your activity for later in the afternoon you can take advantage of the incredible sunset while relaxing on the boat for half an hour. Sea sickness? usually not a problem as the boats tend to stay closer into the shore and cut through the waves very well.  Paraw sailing around Boracay is probably a really good way to ease yourself into the sea and find out how much you like it.",
            "image_url": "https://cdn5.myboracayguide.com/2016/03/Paraw-Sailing-Boracay-Activities-400x267.jpg",
            "price": "3000"
        }, ......
..............................
more data
..............................
	]
}
```
- Test Get Product
```
curl -X GET \
  http://localhost:8080/products/8f086c95-df7d-4914-98b5-e3378663e967 \
  -H 'Host: localhost:8080' 
```
```
 {
     "id": "8f086c95-df7d-4914-98b5-e3378663e967",
     "name": "Paraw Sailing",
     "description": "Paraw Sailing is a local sail boat activity. The boats use two outriggers and two sails. Experience the traditional way of sailing and discover the best sites around the island, perfect for photography – though do note on days with heavier waves the water can kick up a bit (exciting!). If you schedule your activity for later in the afternoon you can take advantage of the incredible sunset while relaxing on the boat for half an hour. Sea sickness? usually not a problem as the boats tend to stay closer into the shore and cut through the waves very well.  Paraw sailing around Boracay is probably a really good way to ease yourself into the sea and find out how much you like it.",
     "image_url": "https://cdn5.myboracayguide.com/2016/03/Paraw-Sailing-Boracay-Activities-400x267.jpg",
     "price": "3000"
 }
```
- Test Create Product
```
curl -X POST \
  http://localhost:8080/products \
  -H 'Content-Type: application/json' \
  -d ' {
          "name": "4 Hour Private Boracay Island Hopping Package",
          "description": "Your Boracay adventure experience will not be complete without this trip! The island is home to more than a dozen undeveloped beaches, turquoise waters and colorful coral reefs! Feast your eyes on the amazing scenery, snorkel and get a glimpse of the thriving sea life!The boat trip includes stopover at some amazing places in Boracay where you can go snorkeling and swimming. Snorkeling gears will be provided for you.",
          "image_url": "https://cdn5.myboracayguide.com/2016/09/Private-Island-Hopping-Boracay-Activity-8-400x267.jpg",
          "price": 2900
        }'
```
```
{
    "id": "42cca4c2-b7e1-4daa-aa48-fdf74e32ba97",
    "name": "4 Hour Private Boracay Island Hopping Package",
    "description": "Your Boracay adventure experience will not be complete without this trip! The island is home to more than a dozen undeveloped beaches, turquoise waters and colorful coral reefs! Feast your eyes on the amazing scenery, snorkel and get a glimpse of the thriving sea life!The boat trip includes stopover at some amazing places in Boracay where you can go snorkeling and swimming. Snorkeling gears will be provided for you.",
    "image_url": "https://cdn5.myboracayguide.com/2016/09/Private-Island-Hopping-Boracay-Activity-8-400x267.jpg",
    "price": "2900",
    "status": "CREATED OK"
}
```
- Test Update Product
```
curl -X PUT \
  http://localhost:8080/products/2178bb44-32f1-4d22-bc95-05cd039a3067 \
  -H 'Content-Type: application/json' \
  -d ' {
         "name": "4 Hour Private Boracay Island Hopping Package",
         "description": "Your Boracay adventure experience will not be complete without this trip! The island is home to more than a dozen undeveloped beaches, turquoise waters and colorful coral reefs! Feast your eyes on the amazing scenery, snorkel and get a glimpse of the thriving sea life!The boat trip includes stopover at some amazing places in Boracay where you can go snorkeling and swimming. Snorkeling gears will be provided for you.",
         "image_url": "https://cdn5.myboracayguide.com/2016/09/Private-Island-Hopping-Boracay-Activity-8-400x267.jpg",
         "price": 2900
        }'
```
```
{
    "name": "4 Hour Private Boracay Island Hopping Package",
    "description": "Your Boracay adventure experience will not be complete without this trip! The island is home to more than a dozen undeveloped beaches, turquoise waters and colorful coral reefs! Feast your eyes on the amazing scenery, snorkel and get a glimpse of the thriving sea life!The boat trip includes stopover at some amazing places in Boracay where you can go snorkeling and swimming. Snorkeling gears will be provided for you.",
    "image_url": "https://cdn5.myboracayguide.com/2016/09/Private-Island-Hopping-Boracay-Activity-8-400x267.jpg",
    "price": "2900",
    "status": "UPDATED OK"
}
```

- Test Delete Product
```
curl -X DELETE \
  http://localhost:8080/products/2178bb44-32f1-4d22-bc95-05cd039a3067 \
  -H 'Content-Type: application/json' 
```
```
{
    "id": "2178bb44-32f1-4d22-bc95-05cd039a3067",
    "status": "DELETED OK"
}
```

## Step 2: Setup Dynamodb for Production

### TODO

### (Optional) Clean up
```
$ aws ecr delete-repository --repository-name myproject-product-restapi --force
$ aws codecommit delete-repository --repository-name myproject-product-restapi
$ rm -rf ~/environment/myproject-product-restapi
```
