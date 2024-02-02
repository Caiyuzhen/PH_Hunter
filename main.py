from flask import Flask, request, jsonify, send_from_directory
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import io
import os
import json
import random
from dotenv import load_dotenv # 用来加载环境变量

load_dotenv()  # 加载 .env 文件中的环境变量
PH_TOKEN = os.environ.get('PH_TOKEN')
HOST = os.environ.get('HOST')
app = Flask(__name__)


# 定义 GraphQL 查询
query = gql('''
	query todayPosts {
		posts(order: FEATURED_AT, featured: true, topic: "artificial-intelligence") {
			edges {
				node {
					name
					description
					votesCount
					url
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
 
 	# 从【查询结果】内提取帖子主体
	posts_edges = response['posts']['edges']
 
     # 如果帖子列表不为空，随机选择一篇帖子
	if posts_edges:
		# 返回全部 post
		# return response

		# 随机选择三篇 post 返回
		num_posts = min(3, len(posts_edges))
  
		# 随机选择 num_posts 篇帖子
		selected_posts = random.sample(posts_edges, num_posts)
  
		# 更新响应结构以仅包含选定的帖子
		response['posts']['edges'] = selected_posts

		# 随机选择一篇 post 返回
		# random_post = random.choice(posts_deges)['node']
		# 将随机选中的帖子包装在相同的结构中返回
		# response['posts']['edges'] = [{'node': random_post}]
	else:
		# 如果没有帖子，确保返回的结构是空的
		response['posts']['edges'] = []
  
	return response


# 定义 API 路由
@app.route('/todayPosts', methods=['GET'])
def get_today_posts():
    return jsonify(queryPH_everyDay())

if __name__ == "__main__":
    app.run(host=HOST, port=6666)