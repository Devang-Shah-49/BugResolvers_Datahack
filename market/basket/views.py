import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.cluster import KMeans
from .serializers import AssociationRulesSerializer, MarketBasketChartsSerializer, RFMTableSerializer, UserSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from .models import AssociationRules, MarketBasketCharts, RFMTable, User, Product, Order, OrderItem, Coupon

from django.core.mail import EmailMessage
from django.conf import settings

import datetime
import random
import string

def generate_code(format, length):
    coupon_code = ''
    if format == 'numeric':
        while True:
            coupon_code = ''.join(random.choices(string.digits, k=length))
            checkk = Coupon.objects.filter(code=coupon_code).exists()
            if checkk == False:
                break
    elif format == 'alphabetic':
        while True:
            coupon_code = ''.join(random.choices(string.ascii_uppercase, k=length))
            checkk = Coupon.objects.filter(code=coupon_code).exists()
            if checkk == False:
                break

    elif format == 'alphanumeric':
        while True:
            coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            checkk = Coupon.objects.filter(code=coupon_code).exists()
            if checkk == False:
                break
    return coupon_code

def send_email(data):
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[
                         data['to_email']], from_email=settings.EMAIL_HOST_USER)
    email.send()

@api_view(['GET'])
def get_user(request):
    reader = pd.read_csv(r'market\jetson-sample-data.csv')
    for i in range(len(reader["client_id"])):
        slist = reader["date"][i].split("-")
        sdate = datetime.date(int(slist[0]),int(slist[1]),int(slist[2]))
        user,k = User.objects.get_or_create(client_id=reader["client_id"][i], email='devangvshah16@gmail.com', first_name="User")
        if k:
            user.set_password("12345678")
            user.last_name=i
        user.last_transaction=sdate
        user.save()
        if slist[1] in ["01","02","03"]:
            season = "Winter"
        elif slist[1] in ["04","05","06"]:
            season = "Summer"
        elif slist[1] in ["07","08","09"]:
            season = "Spring"
        else:
            season = "Fall"
        product,k = Product.objects.get_or_create(item_name=reader["item_name"][i])
        if k:
            product.price = reader["price"][i]
            product.season = season
            product.save()
        order,k = Order.objects.get_or_create(order_id=reader["order_id"][i], client_id=user, order_date=sdate)
        if k:
            order.save()
        order_item,k = OrderItem.objects.get_or_create(order=order, item_name=product)
        if k:
            order_item.quantity = 0
        order_item.quantity += reader["quantity"][i]
        order_item.save()
    return Response({"success":"success"})

@api_view(['GET'])
def send_codes(request):
    sent = 0
    inactive_users = User.objects.filter(last_transaction__lte=datetime.date.today()-datetime.timedelta(days=30))
    #print(inactive_users.values_list('last_transaction', flat=True))
    for user in inactive_users:
        coupon = Coupon.objects.create(user=user, code=generate_code('alphanumeric', 6), discount_value=random.randint(10, 50), expiry_date=datetime.date.today()+datetime.timedelta(days=30))
        data = {
            'to_email': user.email,
            'email_subject': 'Coupon Code for your next order!',
            'email_body': f'Your coupon code is {coupon.code} and it is valid till {coupon.expiry_date}.'
        }
        #send_email(data)
        #gpt_query("Which items have revenue greater than $200?")
        sent = 1
        if sent == 1:
            return Response({"Inactive Count":f"{len(inactive_users)}", "Sent":f"{sent}"})
    return Response({"success":"success"})


# !pip install langchain
# !pip install duckdb
# !pip install unstructured
# !pip install chromadb
# !pip install BeautifulSoup4
# !pip install openai
import csv
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from langchain.chains import VectorDBQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.unstructured import UnstructuredFileLoader 
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def gpt_query(question):
#   loader = UnstructuredFileLoader(file_path=r'market\sales_data_preprocessed.txt')
#   documents = loader.load()
#   documents = loader.load()
  embeddings = OpenAIEmbeddings(openai_api_key="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")
#   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#   texts = text_splitter.split_documents(documents)
#   db = Chroma.from_documents(texts, embeddings,persist_directory = r'market\devang')
#   db.persist()
  vectordb = Chroma(persist_directory=r'market\devang',embedding_function=embeddings)
  qa = VectorDBQA.from_chain_type(llm=ChatOpenAI(openai_api_key="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"), chain_type="stuff", vectorstore=vectordb, k=10)
  return str(qa.run(question))

@api_view(['POST'])
def get_query(request):
    question = request.data['question']
    return Response({"answer":gpt_query(question)})

def num(x):
    if x <= 0:
        return 0
    elif x >=1:
        return 1

def analyse():
    df = pd.read_csv(r'market\jetson-sample-data.csv')
    data_apr = df.groupby(["order_id", "item_name"])[["quantity"]].sum().unstack().reset_index().fillna(0).set_index("order_id")
    basket_new = data_apr["quantity"].applymap(num)
    apr = apriori(basket_new, min_support = 0.02, use_colnames = True)
    apr = apr.sort_values(by = "support", ascending = False)
    end = association_rules(apr, metric = "lift", min_threshold = 1)
    end = end.sort_values(by = "confidence", ascending = False)
    return end

@api_view(['GET'])
def rfm_table(request):
    '''df = pd.read_csv('jetson-sample-data.csv')
    today = datetime.datetime.today()
    df["date"] = pd.to_datetime(df["date"])
    rec_table = df.groupby(["client_id"]).agg({"date": lambda x: ((today - x.max()).days)})
    rec_table.columns = ["Recency"]
    freq_table = df.drop_duplicates(subset = "order_id").groupby(["client_id"])[["order_id"]].count()
    freq_table.columns = ["Frequency"]
    df["Total_Price"] = df["price"]
    monetary_table = df.groupby(["client_id"])[["Total_Price"]].sum()
    monetary_table.columns = ["Monetary"]
    rfm_data = pd.concat([rec_table, freq_table, monetary_table], axis = 1)
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_data)
    kmeans = KMeans(n_clusters = 3)
    kmeans.fit(rfm_scaled)
    rfm_data["Cluster_No"] = (kmeans.labels_ + 1)
    final_df = rfm_data.groupby(["Cluster_No"])[["Recency", "Frequency", "Monetary"]].mean()
    seg = ["premium", "regular", "low"]
    for i in range(3):
        serializer = RFMTableSerializer(data={"rfm_segment":seg[i],"recency":final_df['Recency'][i+1], "frequency":final_df['Frequency'][i+1], "monetary":final_df['Monetary'][i+1]})
        if serializer.is_valid(raise_exception=True):
            serializer.save()'''
    data = RFMTableSerializer(RFMTable.objects.all(), many=True).data
    return Response({"data":data})

def piechart(data,season):
  fig, ax = plt.subplots(figsize=(8, 6))
  colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']
  explode = (0.05, 0.05, 0.05, 0.05, 0.05)
  ax.pie(data.head()['quantity'], labels=data.head()['item_name'], colors=colors, explode=explode, autopct='%1.1f%%', startangle=90)
  ax.set_title(f"Top 5 Items - {season}", fontsize=14, fontweight='bold')
  ax.legend(title="Items", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
  plt.show()

def plots():
    df = pd.read_csv(r'market\jetson-sample-data.csv')
    temp = df['item_name'].value_counts()
    topItems = pd.DataFrame({'Item_Name': temp.index, 'Frequency': temp.values})
    sns.barplot(x = 'Item_Name',y = 'Frequency',data = topItems.head(10))
    plt.xticks(rotation = 90)
    plt.show()
    dateTime = df.groupby('date')['quantity'].sum()
    df1 = pd.DataFrame(dateTime,columns=["quantity"])
    grouped_df = df.groupby(['date'])['item_name'].agg(list).reset_index(name='items_sold')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = grouped_df.date , y = grouped_df.items_sold, mode = "markers"))
    fig.update_layout(yaxis_title=None)
    fig.show()
    grouped_df['month'] = pd.to_datetime(grouped_df['date']).dt.month
    grouped_df['Season'] = grouped_df['month'].apply(lambda x: 'Winter' if x in [1, 2, 12] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Fall')))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = grouped_df.Season , y = grouped_df.month , mode = "markers"))
    fig.update_layout(yaxis_title=None)
    fig.show()
    grouped_df_freq = df.groupby(['date', 'item_name'])['quantity'].sum().reset_index()
    grouped_df_freq['month'] = pd.to_datetime(grouped_df['date']).dt.month
    grouped_df_freq['Season'] = grouped_df['month'].apply(lambda x: 'Winter' if x in [1, 2, 12] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Fall')))
    new = grouped_df_freq.groupby(['item_name','Season'])['quantity'].sum().reset_index()
    fall_df = new.loc[new['Season'] == 'Fall'].copy()
    fall_df = fall_df.sort_values('quantity', ascending=False)
    summer_df = new.loc[new['Season'] == 'Summer']
    summer_df = summer_df.sort_values('quantity', ascending=False)
    winter_df = new.loc[new['Season'] == 'Winter']
    winter_df = winter_df.sort_values('quantity', ascending=False)
    spring_df = new.loc[new['Season'] == 'Spring']
    spring_df = spring_df.sort_values('quantity', ascending=False)
    fall_df = new.loc[new['Season'] == 'Fall'].copy()
    fall_df = fall_df.sort_values('quantity', ascending=False)
    piechart(winter_df,"Winter")
    piechart(summer_df,"Summer")
    piechart(fall_df,"Fall")
    piechart(spring_df,"Spring")
    monthFreq = grouped_df_freq.groupby(['month'])['quantity'].sum()
    monthFreq.to_dict()
    month_list = list(monthFreq.items())
    x_values = [x for x, y in month_list]
    y_values = [y for x, y in month_list]
    plt.plot(x_values, y_values)
    plt.xlabel('Month')
    plt.ylabel('Value')
    plt.title('Line Chart')
    plt.show()

@api_view(['GET'])
def get_data(request):
    '''end = analyse()
    for i in range(len(end["antecedents"])):
        serializer = AssociationRulesSerializer(data={"antecedents":list(end["antecedents"][i]), "consequent":list(end["consequents"][i]), "confidence":end["confidence"][i]})
        if serializer.is_valid(raise_exception=True):
            serializer.save()'''
    rules = AssociationRulesSerializer(AssociationRules.objects.all(), many=True).data
    return Response({"rules":rules})

@api_view(['GET'])
def get_charts(request):
    #plots()
    charts = MarketBasketChartsSerializer(MarketBasketCharts.objects.all(), many=True).data
    return Response({"message":charts})

def average_customer_buy(df):
  customer_spending = df.groupby('client_id')['price'].sum()
  df2 = pd.DataFrame(customer_spending)
  avg_cust_buy = df2['price'].sum() / len(df2)
  return avg_cust_buy

def average_order_cost(df):
  particuar_order_count = df.groupby('order_id')['price'].sum()
  df3 = pd.DataFrame(particuar_order_count)
  avg_order_cost = df3['price'].sum() / len(df3)
  return avg_order_cost

def highest_selling_item_cost(df):
  item_price = df.groupby('item_name')['price'].sum()
  df1 = pd.DataFrame(item_price)
  new = df1.sort_values(by=['price'],ascending=False)
  x = new.iloc[[0]]
  return x

@api_view(['GET'])
def get_stats(request):
    df = pd.read_csv(r'market\jetson-sample-data.csv')
    avg_cust_buy = average_customer_buy(df)
    avg_order_cost = average_order_cost(df)
    highest_selling_item_cst = highest_selling_item_cost(df)
    return Response({"avg_cust_buy":avg_cust_buy, "avg_order_cost":avg_order_cost, "highest_selling_item_cost":highest_selling_item_cst["price"][0]})