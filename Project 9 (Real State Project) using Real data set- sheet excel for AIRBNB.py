'''بسم الله الرحمن الرحيم'''
 
                                             #Project 9 (Real State Project) using Real data set- sheet excel for AIRBNB
#Airbnb: هوة برنامج فى امريكا عقارى..بيوصل الناس اللى بتدور على غرف للإيجار بالناس اللى عندها غرف للايجار
#احنا نزلنا ال data بتاعتهم وهنشتغل عليها
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv('AB_NYC_2019.csv')

data.head()

#column explain:
#1st(ID): ID of hostle
#2end(name): name of the hostel
#3rd(Host_ID): ID of hostle owner
#4th(host_name): name of hostle owner
#5th(neighbourhood_group): stat of where hostle is
#6th(neighbourhood):where hostle is in the stat
#7th(latitude):خط الطول
#8th(longtitude):خط العرض
#9th(room_type):type of room(private room OR entire appartement)
#10(price):price of the room
#11th(minimum_nights):the minimum no of nights in each room
#12th(no of reviews):reviews for each room from members
#13th(last_review):the date of last review
#14th(reviews per month):total reviews per month
#15th(calc_host_list_count):
#16th(availability):how many room availble
#######

#هنخلى السعر فى متغير لوحدة
y=data['price']
#وطبعا هشيل عمود ال price من ال data الرئيسية بس طبعا فى متغير جديد هنسمية ال x
x=data
#هنشيل الاعمدة اللى مالهاش تاثير عندى خالص:
#id,name,host_id,host_name,latitude,longitude
x =x.drop(['id','name','host_id','host_name','price','latitude','longitude'] ,axis=1)
#دلوقتى انا عندى مشكلة : الاسامى الموجودة دلوقتى فى الاعمدة بتاعة ال neighbour وال roomtype وخلافة
#انا محتاج اعمل ليهم زى index كدة عشان يبقى سهل عليا اعرف اعمل تحليلاتى بالارقام
#فهنعمل اية: هنحول ال texts دى ل dummy_variables بمعنى انى هعملهم categroize بمعنى ان كل stat هنديها رقم 0 او 1 او 2 وهكذا
#هنشتغل الاول على neighbourhood_group
df_ngroup = pd.get_dummies(x['neighbourhood_group'])
#دلوقتى عشان نفهم عملنا اية: لو بصينا فى الجدول بتاع ال df_group هنلاقية اخذ كل ال states  بتاعة ال neighbourhood_group وخلاهم اعمدة وتحتهم مجموعة من ال zero & one
#دلوقتى هوة اخدهم وعمل ليك فى اول صف كل واحد اخذ كام : بمعنى ان الصف الاول broklyn كانت واخدة 1 ومافيش اى حد غيرها اخد حاجة
#دلوقتى انا عايز اربط ال df_ngroup الجديد واحطة فى ال x-data
x=pd.concat([x,df_ngroup] , axis=1)
#دلوقتى اتضاف فى اخر جدول ال x ال categorization اللى تم على ال neighbourhood_group
#دلوقتى انا هلغى طبعا العمود بتاع neighbourhood_group من على الdata بتاعة ال x
x=x.drop(['neighbourhood_group'] , axis = 1)
#دلوقتى هنشتغل على عمود ال room_type
df_room=pd.get_dummies(x['room_type'])
x=pd.concat([x,df_room] , axis=1)
x=x.drop(['room_type'] , axis = 1)
#دلوقتى هنشتغل على عمود ال neighbourhood
df_ni=pd.get_dummies(x['neighbourhood'])
#لاقينا ان ال df_ni كبيرة جدا ودة هيصعب علينا ال analysis جدا ..فهنشيلها من حسابتنا
x=x.drop(['neighbourhood'] , axis = 1)
#دلوقتى عايزين نعرف عدد ال NAN فى ال x
x.isna().sum()
#طبعا انا لاقيت رقم مهول لعدد ال cells اللى مالهاش بيانات NAN حوالى 10 الاف فى ال reviews_per_month & last_review
#بالنسبة لل last_review فماينفعش اخد متوسطهم لانها أشهر..بس ممكن اخد اكتر تاريخ مكرر فيهم واملى بية البيانات الفارغة
# او ممكن نملى البيانات دى باقرب بيانات ليها فى الcell بمعنى انة بيبص على الخلية اللى قبلها عالطول (فى نفس العمود) وبيملى بيها القيمة الناقصة
#واحنا هنمشى بالاقتراح الثانى
x['last_review'].fillna(method='ffill',inplace=True)
#ولكن فى التحليل اللى هتعملة مش محتاجين التواريخ الخاصة بال reviews فهمنشيلها
x=x.drop('last_review' , axis = 1)
#ااما بالنسبة لل reviews_per_month فهنا ممكن اخد متوسطهم ال average
x['reviews_per_month'].fillna(x['reviews_per_month'].mean(),inplace=True)
#دلوقتى عايزين نعرف عدد ال NAN فى ال x
x.isna().sum()
#دلوقتى قبل عملية استخدام التحليل محتاج اشوف histogram لل data الرئيسية بتاعتى بدون التعديلات اللى عملتها عشان ابدا احدد عملية التحليلات هنعملها ازاى
#ال data الرئيسية اللتى لم يتم عليها اى تعديل
data.head(3)
#دلوقتى عايزين نرسم histogram للعمود مثلا بتاع ال neighbourhood_group 
#وهنخزن الرسمة فى متغير جديد
data_new=data
x1=sns.countplot(x='neighbourhood_group', data=data_new)
#الرسمة اعتقد واضحة فى ملامحها
#الدكتور بيقول : 
#عشان اعمل عنوان لل chart
plt.title('Popular neighbourhood group')
#عشان اعمل label بمعنى اسم لل x_axis
plt.xlabel('Neighbourhood Group')
#عشان اعمل اسم لل y_axis
plt.ylabel('Count')
plt.show
#فهمنا من الرسمة محتاجين نفتكر ال neighbourhood_group كان عبارة عن اية: كان مكان الفندق فى ال state 
#هنا بيقولك تعداد الفنادق بكل ولاية وظاهر لينا من الرسمة ان اكتر تكتل للفنادق فى ولاية مانهاتن و بروكلين
###
#تعالوا دلوقتى نشوف ال room_type فى الرسمة
x1=sns.countplot(x='room_type', data=data_new)
plt.title('Room Type Distribution')
plt.xlabel('Room Type')
plt.ylabel('Frequency')
plt.show
# اكثر رووم تم سكنها من قّبل الفنادق كانت ال entire home
#دلوقتى عايزين نعرف علاقة ال room_type بال neighbourhood_group 
#زى ماشرحنا فى البروجيكت اللى قبلة
#عشان احدد حجم ال column
plt.figure(figsize=(10,10))
x1=sns.countplot(x='room_type', data=data_new,hue= 'neighbourhood_group')
#دلوقتى لاحظنا انة قسملى ال private&entire&shared فى ال x_label 
#دلوثتى لاحظنا ان فى مانهاتن ال entire واخدة صوت عالى جدا فالافضل طبعا لو هروح مانهاتن اكيد هاجر شقة كاملة
#اما بالنسبة لو هاجر "برايف رووم" فالافضل اروح بروكلين
####
#دلوقتى انا عايز اعرف بالنسبة لعلاقة الاسعار وال neighbourhood group 
#وابين فيها ال outlayers : بمعنى اية الاسعار الفارقة عن المعتاد والخارجة عن المالوف فى اى مدينة
#وعشان اعرف اطلع ال outlayers فى الاسعار مقارنة بال states
sns.boxplot(x='neighbourhood_group',y='price',data=data_new)
#لو بصينا على ال queens هنلاقى فية outlayers بعيدة جدا عن تجمع الداتا تحت خالص
#وهكذا فى ال staten island
#وهكذا فى مانهاتن وبروكلين
#فدلوقتى انا عايز اطلع ال outlayers دول خالص 
??????????????????????????????????????????????????????????
data_price = data_new(data_new['price'] <= 400)
#كدة انا قولتلة اى سعر مساوى او اكبر من 400 هيتحط فى ال data_price
data.price.plot(kind='hist')