from fastapi import FastAPI,Path,Query
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse
#创建 FastAPI实例
app = FastAPI()

@app.get("/")
async def root():    # 定义根路径的路由    由async定义的函数返回JSON响应
    return {"message": "Hello World"}

#访问 /hello

# @app.get("/hello")     # app是FastAPI实例，get是请求方法，"/hello"是路径，定义了访问的路径
# async def get_hello():
#     return {"msg":"你好 FastAPI"}  # 返回JSON响应结果msg:你好 FastAPI

# 为什么要创建虚拟环境?
# 隔离项目运行环境，避免依赖冲突，保持全局环境的干净和稳定
#
# 怎么运行FastAPI项目?
# run项目
# uvicorn main:app --reload      --reload:更改代码后自动重启服务器
#
# 怎么访问FastAPI交互式文档?
# http://127.0.0.1:8000/docs


# 路由
# 路由就是URL 地址和处理函数之间的映射关系，
# 它决定了当用户访问某个特定网址时，服务器应该执行哪段代码来返回结果。

# 练习
# @app.get("/user/hello")     # app是FastAPI实例，get是请求方法，"/hello"是路径，定义了访问的路径
# async def get_hello():
#     return {"msg":"我正在学习FastAPI....."}  # 返回JSON响应结果msg:我正在学习FastAPI....

# @app.get("/book/{id}")#传入路径参数id
# async def get_book(id: int=Path(...,gt=0,lt=101,description="书籍id,取值范围1-100之间")):# 定义路径参数id的类型为int
#     return {"id": id,"title":f"这是第{id}本书"}


#
# @app.get("/author/{name}")
# async def get_author(name: str=Path(...,min_length=2,max_length=10,description="作者姓名")):# 定义路径参数name的类型为str
#     return {"msg":f"作者姓名是{name}"}

# 路径参数出现在什么位置?
# URL 路径的一部分  /book/{id}
# 如何为路径参数添加类型注解?
# Python原生注解和Path注解


# 查询参数  声明的参数不是路径参数时，路径操作函数会把该参数自动解释为查询参数
# 位置:URL?之后
#  k1=v1&k2=v2
#  作用:对资源集合进行过滤、排序、分页等操作
# 方法:GET


#需求查询新闻>分页，skip:跳过的记录数  limit:返回的记录数 10
# @app.get("/news/news_list")
# async def get_news_list(
#         skip: int=Query(0,gt=-1,description="跳过的记录数"),
#         limit: int=Query(10,gt=0,lt=101,description="返回的记录数")):
#     return {"skip":skip,"limit":limit}

@app.get("/news/news_list")
async def get_news_list(
        category: str=Query("Python开发",max_length=255,min_length=5,description="图书分类"),
        price: float=Query(...,lt=101.0,gt=49.0)):
    return {"category":category,"price":price}


# 请求体
# 位置:HTTP请求的消息体 (body)中
# 作用:创建、更新资源 携带大量数据，如:JSON
# 方法:POST、PUT等

# 在HTTP协议中，一个完整的请求由三部分组成:
# 请求行:包含方法、URL、协议版本
# 请求头:元数据信息(Content-Type、Authorization等)
# 请求体:实际要发送的数据内容


# 注册：用户名和密码  -->str

# class User(BaseModel):
#     username: str
#     password: str
#
# @app.post("/register")
# async def register(user: User):
#     return {"msg":f"注册成功，用户名:{user.username}密码:{user.password}"}

# 需求:设计接口新增图书，图书信息包含:书名、作者、出版社、售价

# 创建了一个名为 Book 的 Pydantic 模型类
# class Book(BaseModel):
#     book_name: str
#     author: str
#     publisher: str
#     price: float
#
# @app.post("/book")
# async def book(book: Book):
#     # 使用 @app.post("/book") 装饰器注册一个 POST 请求处理器
#     # 端点路径为 /book
#     # 函数接收一个 Book 类型的参数，FastAPI 会自动将请求体中的 JSON 数据解析为 Book 对象
#     # 函数是异步的（async）
#     return {"msg":f"新增图书成功，书名:{book.book_name}作者:{book.author}出版社:{book.publisher}售价:{book.price}"}
#     # 返回一个 JSON 响应
#     # 响应消息中包含从请求中接收到的所有图书信息
#     # 使用 f-string 格式化字符串，将图书的各个属性值嵌入到返回消息中
#
# # 请求体参数-类型注解Field
# # 导入pydantic的Field函数
# from pydantic import BaseModel, Field
# class User(BaseModel):
#     username: str = Field(default="张三",min_length=2,max_length=10,description="用户名,长度要求2-10")
#     password: str = Field(default="123456",min_length=6,max_length=20,description="密码,长度要求6-20")
#
# @app.post("/register")
# async def User(user: User):
#     return user    # 返回JSON响应结果

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
# # 响应类型
# # 默认情况下，FastAPI会自动将路径操作函数返回的Python对象(字典、列表、Pydantic 模型等)，经由jsonable_encoder 转换为JSON兼容格式，
# # 并包装为JSONResponse 返回。这省去如果需要返回非JSON数据(如HTML、文件流)，FastAPI 提供了丰富的响应类型来返回不同数据
#
# @app.get("/html",response_class=HTMLResponse)
# async def html():
#     return "<h1>这是一级标题</h1>"


# 响应文件格式
# FileResponse 是FastAPI 提供的专门用于高效返回文件内容的推荐方式。、媒体类型推断、范围请求和缓存头部，是服务静态文件
# 内容(如图片、PDF、Excel、音视频等)的响应类。它能够智能处理文件路径，自动设置正确的响应头，如Content-Type、Content-Length等。

# @app.get("/file")
# async def file():
#     path="./files/cat.jpg"
#     return FileResponse(path)


# 自定义响应数据格式
#
# response_model 是路径操作装饰器(如@app.get域@app.post)的关键参数，它通过一个Pydantic模型来严格定义和约束API端点的输出格式，
# 。这一机制在提供自动数据验证和序列化的同时，更是保障数据安全性的第一道防线。

# 需求：新闻接口->相应数据格式   id、title、content
# class News(BaseModel):
#     id: int
#     content: str
#     title: str
# @app.get("/news/{id}",response_model=News)
# async def get_news(id: int):
#     return (
#         {"id": id,
#         "title": f"这是第{id}条新闻",
#         "content": f"这是第{id}条新闻的内容"}
#     )


# 异常处理
# 对于客户端引发的错误(4xx，如资源未找到、认证失败)，应使用fastapi.HTTPException来中断正常处理流程，
# 并返回标准错误响应。
# 对于服务器引发的错误(5xx，如内部错误、服务不可用)，应使用fastapi.HTTPException来中断正常处理流程，
# 并返回标准错误响应。

from fastapi import HTTPException

#需求按id查询新闻
@app.get("/news/{news_id}")
async def read_news(news_id: int):
    id_list=[1,2,3]
    if news_id not in id_list:
        raise HTTPException(status_code=404, detail="News not found")
    return {"news_id": news_id}

