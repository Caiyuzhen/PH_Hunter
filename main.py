from flask import Flask, request, jsonify, send_from_directory
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import io
import os
import json
from dotenv import load_dotenv # 用来加载环境变量

load_dotenv()  # 加载 .env 文件中的环境变量
PH_TOKEN = os.environ.get('PH_TOKEN')
HOST = os.environ.get('HOST')
app = Flask(__name__)


# 定义 GraphQL 查询
query = gql('''
query todayPosts {
	posts {
		edges {
			node {
				id
				name
				tagline
				votesCount
				url
                thumbnail {
					url
				}
				media {
					type
					url
				}
			}
		}
	}
}
''')


# 构建查询方法
def queryPH_everyDay():
	print("👍 获得了 token:", PH_TOKEN)
	# 设置 GraphQL 客户端的参数
	transport = RequestsHTTPTransport(
		url='https://api.producthunt.com/v2/api/graphql',
		headers={
			'Authorization': f'Bearer {PH_TOKEN}'
		},
		use_json=True,
	)

	# 实例化客户端
	client = Client(transport=transport, fetch_schema_from_transport=True)
    
	# 执行查询
	response = client.execute(query)
	return response


# 定义 API 路由
@app.route('/todayPosts', methods=['GET'])
def get_today_posts():
    return jsonify(queryPH_everyDay())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)