import requests
import json

async def get_rare_strong_unit():
  url = "https://api-gateway.skymavis.com/graphql/mavis-marketplace"

  headers = {"X-API-KEY": "4EI6PfiWc4dP2uFtiN6Vruf6pEYABJh7"}

  body = """ 
  query MyQuery {
    erc721Tokens(
      from: 0
      size: 30
      tokenAddress: "0xa038c593115f6fcd673f6833e15462b475994879"
      auctionType: Sale
      sort: Latest
    ) {
      results {
        attributes
        tokenId
        order {
          currentPrice
        }
        image
      }
    }
    exchangeRate {
      ron {
        usd
      }
    }
  }
  """
  strong_unit = {"pigcopter":1.5, "zeppelin":1.5, "ninja":5, "glider":1.2, "mousefly":1.2, 
                "skeleton": 1, "archer": 2.1, "thundercaster": 1.1, "storm cat": 1.1, "tank": 3}

  response = requests.post(url=url, headers=headers, json={"query": body}) 
  print("response status code: ", response.status_code) 

  my_bytes_value = response.content
  my_json = my_bytes_value.decode('utf8').replace("'", '"')

  data = json.loads(my_json)
  list_listing = data["data"]["erc721Tokens"]["results"]
  ron_rate = data["data"]["exchangeRate"]["ron"]["usd"]
  list_unit = []

  for unit in list_listing:
      

      attributes = unit["attributes"]
      if attributes is None : continue

      order = unit["order"]
      name = attributes["type"][0]
      rarity = attributes["rarity"][0]
      price = int(order["currentPrice"])/1000000000000000000
      image = unit["image"]
      link = "https://marketplace.skymavis.com/collections/0xa038c593115f6fcd673f6833e15462b475994879/" + unit["tokenId"]
      tokenId = unit["tokenId"]

      if attributes is None or rarity != 'rare': continue
      if name not in list(strong_unit.keys()): continue
      
      list_unit.insert(0, [name, rarity, price, link, image, tokenId])
  return list_unit, ron_rate

  # for i in list_unit:
  #     if i[2] <= strong_unit[i[0]]: print(i)
  #     else: print("expensive: ", i)
