# Databricks notebook source
# MAGIC %md
# MAGIC <img src="http://data.freehdw.com/ships-titanic-vehicles-best.jpg"  Width="800">

# COMMAND ----------

# MAGIC %md
# MAGIC <a id="introduction" ></a><br>
# MAGIC This kernel is for all aspiring data scientists to learn from and to review their knowledge. We will have a detailed statistical analysis of Titanic data set along with Machine learning model implementation. I am super excited to share my first kernel with the Kaggle community. As I go on in this journey and learn new topics, I will incorporate them with each new updates. So, check for them and please <b>leave a comment</b> if you have any suggestions to make this kernel better!! Going back to the topics of this kernel, I will do more in-depth visualizations to explain the data, and the machine learning classifiers will be used to predict passenger survival status.
# MAGIC 
# MAGIC <div style="text-align: left"> 
# MAGIC     <br>
# MAGIC     NOTE:
# MAGIC     <ul>
# MAGIC         <li>Follow me on <a href="https://www.youtube.com/channel/UC1mPjGyLcZmsMgZ8SJgrfdw"><b>YOUTUBE</b></a> to get the video tutorial for this notebook.
# MAGIC         <li>If you want to learn more about Advanced Regression models, please check out <a href="https://www.kaggle.com/masumrumi/a-stats-analysis-and-ml-workflow-of-house-pricing">this</a> kernel.</li>
# MAGIC         <li>If you are reading this on github, I recommend you read this on <a href="https://www.kaggle.com/masumrumi/a-statistical-analysis-ml-workflow-of-titanic">kaggle</a>.</li>
# MAGIC     </ul>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Kernel Goals
# MAGIC <a id="aboutthiskernel"></a>
# MAGIC ***
# MAGIC There are three primary goals of this kernel.
# MAGIC - <b>Do a statistical analysis</b> of how some group of people was survived more than others. 
# MAGIC - <b>Do an exploratory data analysis(EDA)</b> of titanic with visualizations and storytelling.  
# MAGIC - <b>Predict</b>: Use machine learning classification models to predict the chances of passengers survival.
# MAGIC 
# MAGIC P.S. If you want to learn more about regression models, try this [kernel](https://www.kaggle.com/masumrumi/a-stats-analysis-and-ml-workflow-of-house-pricing/edit/run/9585160).

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 1: Importing Necessary Libraries and datasets
# MAGIC ***
# MAGIC <a id="import_libraries**"></a>
# MAGIC ## 1a. Loading libraries
# MAGIC 
# MAGIC Python is a fantastic language with a vibrant community that produces many amazing libraries. I am not a big fan of importing everything at once for the newcomers. So, I am going to introduce a few necessary libraries for now, and as we go on, we will keep unboxing new libraries when it seems appropriate.

# COMMAND ----------

# Import necessary modules
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

%matplotlib inline 
# %config InlineBackend.figure_format = 'retina' ## This is preferable for retina display. 

import warnings ## importing warnings library. 
warnings.filterwarnings('ignore') ## Ignore warning



import os ## imporing os
print(os.listdir("../input/"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1b. Loading Datasets
# MAGIC <a id="load_data"></a>
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC After loading the necessary modules, we need to import the datasets. Many of the business problems usually come with a tremendous amount of messy data. We extract those data from many sources. I am hoping to write about that in a different kernel. For now, we are going to work with a less complicated and quite popular machine learning dataset.

# COMMAND ----------

## Importing the datasets
train = pd.read_csv("../input/titanic/train.csv")
test = pd.read_csv("../input/titanic/test.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC You are probably wondering why two datasets? Also, Why have I named it "train" and "test"?  To explain that I am going to give you an overall picture of the supervised machine learning process. 
# MAGIC 
# MAGIC "Machine Learning" is simply "Machine" and "Learning". Nothing more and nothing less. In a supervised machine learning process, we are giving machine/computer/models specific inputs or data(text/number/image/audio) to learn from aka we are training the machine to learn certain aspects based on the data and the output. Now, how can we determine that machine is actually learning what we are try to teach? That is where the test set comes to play. We withhold part of the data where we know the output/result of each datapoints, and we use this data to test the trained models.  We then compare the outcomes to determine the performance of the algorithms. If you are a bit confused thats okay. I will explain more as we keep reading. Let's take a look at sample datasets.

# COMMAND ----------

train.head()

# COMMAND ----------

temp = train.groupby("Sex")['Age'].min().to_frame().reset_index()

# COMMAND ----------

temp

# COMMAND ----------

temp = temp.rename(columns={"Age": "min_age"})

# COMMAND ----------

temp

# COMMAND ----------

train.head()

# COMMAND ----------

train.dtypes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1c. A Glimpse of the Datasets. 
# MAGIC <a id="glimpse"></a>
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC # Train Set

# COMMAND ----------

# MAGIC %%time
# MAGIC train.sample(5)

# COMMAND ----------

# MAGIC %md
# MAGIC # Test Set

# COMMAND ----------

## Take a look at the overview of the dataset. 
%timeit test.sample(5)

# COMMAND ----------

# MAGIC %md
# MAGIC This is a sample of train and test dataset. Lets find out a bit more about the train and test dataset.

# COMMAND ----------

print ("The shape of the train data is (row, column):"+ str(train.shape))
print (train.info())
print ("The shape of the test data is (row, column):"+ str(test.shape))
print (test.info())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1d. About This Dataset
# MAGIC <a id="aboutthisdataset"></a>
# MAGIC ***
# MAGIC The data has split into two groups:
# MAGIC 
# MAGIC - training set (train.csv)
# MAGIC - test set (test.csv)
# MAGIC 
# MAGIC ***The training set includes our target variable(dependent variable), passenger survival status***(also known as the ground truth from the Titanic tragedy) along with other independent features like gender, class, fare, and Pclass. 
# MAGIC 
# MAGIC The test set should be used to see how well our model performs on unseen data. When we say unseen data, we mean that the algorithm or machine learning models have no relation to the test data. We do not want to use any part of the test data in any way to modify our algorithms; Which are the reasons why we clean our test data and train data separately. ***The test set does not provide passengers survival status***. We are going to use our model to predict passenger survival status.
# MAGIC 
# MAGIC Now let's go through the features and describe a little. There is a couple of different type of variables, They are...
# MAGIC 
# MAGIC ***
# MAGIC **Categorical:**
# MAGIC - **Nominal**(variables that have two or more categories, but which do not have an intrinsic order.)
# MAGIC    > - **Cabin**
# MAGIC    > - **Embarked**(Port of Embarkation)
# MAGIC             C(Cherbourg)
# MAGIC             Q(Queenstown) 
# MAGIC             S(Southampton)
# MAGIC         
# MAGIC - **Dichotomous**(Nominal variable with only two categories)
# MAGIC    > - **Sex**
# MAGIC             Female
# MAGIC             Male
# MAGIC - **Ordinal**(variables that have two or more categories just like nominal variables. Only the categories can also be ordered or ranked.)
# MAGIC    > - **Pclass** (A proxy for socio-economic status (SES)) 
# MAGIC             1(Upper)
# MAGIC             2(Middle) 
# MAGIC             3(Lower)
# MAGIC ***
# MAGIC **Numeric:**
# MAGIC - **Discrete**
# MAGIC   >  - **Passenger ID**(Unique identifing # for each passenger)
# MAGIC   >  - **SibSp**
# MAGIC   >  - **Parch**
# MAGIC   >  - **Survived** (Our outcome or dependent variable)
# MAGIC             0
# MAGIC             1
# MAGIC - **Continous**
# MAGIC >  - **Age**
# MAGIC >  - **Fare**
# MAGIC ***
# MAGIC **Text Variable**
# MAGIC > - **Ticket** (Ticket number for passenger.)
# MAGIC > - **Name**(  Name of the passenger.)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1e. Tableau Visualization of the Data
# MAGIC <a id='tableau_visualization'></a>
# MAGIC ***
# MAGIC I have incorporated a tableau visualization below of the training data. This visualization... 
# MAGIC * is for us to have an overview and play around with the dataset. 
# MAGIC * is done without making any changes(including Null values) to any features of the dataset.
# MAGIC ***
# MAGIC Let's get a better perspective of the dataset through this visualization.

# COMMAND ----------

# MAGIC %%HTML
# MAGIC <div class='tableauPlaceholder' id='viz1516349898238' style='position: relative'><noscript><a href='#'><img alt='An Overview of Titanic Training Dataset ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ti&#47;Titanic_data_mining&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Titanic_data_mining&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ti&#47;Titanic_data_mining&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1516349898238');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>

# COMMAND ----------

# MAGIC %md
# MAGIC We want to see how the left vertical bar changes when we filter out unique values of certain features. We can use multiple filters to see if there are any correlations among them. For example, if we click on **upper** and **Female** tab, we would see that green color dominates the bar with a ratio of 91:3 survived and non survived female passengers; a 97% survival rate for females. We can reset the filters by clicking anywhere in the whilte space. The age distribution chart on top provides us with some more info such as, what was the age range of those three unlucky females as the red color give away the unsurvived once. If you would like to check out some of my other tableau charts, please click [here.](https://public.tableau.com/profile/masum.rumi#!/)

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 2: Overview and Cleaning the Data
# MAGIC <a id="cleaningthedata"></a>
# MAGIC ***
# MAGIC ## 2a. Overview

# COMMAND ----------

# MAGIC %md
# MAGIC Datasets in the real world are often messy, However, this dataset is almost clean. Lets analyze and see what we have here.

# COMMAND ----------

## saving passenger id in advance in order to submit later. 
passengerid = test.PassengerId
## We will drop PassengerID and Ticket since it will be useless for our data. 
#train.drop(['PassengerId'], axis=1, inplace=True)
#test.drop(['PassengerId'], axis=1, inplace=True)

print (train.info())
print ("*"*40)
print (test.info())

# COMMAND ----------

# MAGIC %md
# MAGIC It looks like, the features have unequal amount of data entries for every column and they have many different types of variables. This can happen for the following reasons...
# MAGIC * We may have missing values in our features.
# MAGIC * We may have categorical features. 
# MAGIC * We may have alphanumerical or/and text features.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2b. Dealing with Missing values
# MAGIC <a id="dealwithnullvalues"></a>
# MAGIC ***
# MAGIC **Missing values in *train* dataset.**

# COMMAND ----------

# Let's write a functin to print the total percentage of the missing values.(this can be a good exercise for beginners to try to write simple functions like this.)
def missing_percentage(df):
    """This function takes a DataFrame(df) as input and returns two columns, total missing values and total missing values percentage"""
    total = df.isnull().sum().sort_values(ascending = False)
    percent = round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2)
    return pd.concat([total, percent], axis=1, keys=['Total','Percent'])

# COMMAND ----------

# MAGIC %timeit -r2 -n10 missing_percentage(train) # setting the number of runs(-r) and/or loops (-n)

# COMMAND ----------

missing_percentage(train)

# COMMAND ----------

# MAGIC %md
# MAGIC **Missing values in *test* set.**

# COMMAND ----------

# MAGIC %%timeit -r2 -n10 
# MAGIC missing_percentage(test)

# COMMAND ----------

missing_percentage(test)

# COMMAND ----------

# MAGIC %md
# MAGIC We see that in both **train**, and **test** dataset have missing values. Let's make an effort to fill these missing values starting with "Embarked" feature.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Embarked feature
# MAGIC ***

# COMMAND ----------

def percent_value_counts(df, feature):
    """This function takes in a dataframe and a column and finds the percentage of the value_counts"""
    percent = pd.DataFrame(round(df.loc[:,feature].value_counts(dropna=False, normalize=True)*100,2))
    ## creating a df with th
    total = pd.DataFrame(df.loc[:,feature].value_counts(dropna=False))
    ## concating percent and total dataframe

    total.columns = ["Total"]
    percent.columns = ['Percent']
    return pd.concat([total, percent], axis = 1)
    

# COMMAND ----------

percent_value_counts(train, 'Embarked')

# COMMAND ----------

percent_value_counts(train, 'Embarked')

# COMMAND ----------

# MAGIC %md
# MAGIC It looks like there are only two null values( ~ 0.22 %) in the Embarked feature, we can replace these with the mode value "S". However, let's dig a little deeper. 
# MAGIC 
# MAGIC **Let's see what are those two null values**

# COMMAND ----------

train[train.Embarked.isnull()]

# COMMAND ----------

# MAGIC %md
# MAGIC We may be able to solve these two missing values by looking at other independent variables of the two raws. Both passengers paid a fare of $80, are of Pclass 1 and female Sex. Let's see how the **Fare** is distributed among all **Pclass** and **Embarked** feature values

# COMMAND ----------

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(16,12),ncols=2)
ax1 = sns.boxplot(x="Embarked", y="Fare", hue="Pclass", data=train, ax = ax[0]);
ax2 = sns.boxplot(x="Embarked", y="Fare", hue="Pclass", data=test, ax = ax[1]);
ax1.set_title("Training Set", fontsize = 18)
ax2.set_title('Test Set',  fontsize = 18)


# ## Fixing legends
# leg_1 = ax1.get_legend()
# leg_1.set_title("PClass")
# legs = leg_1.texts
# legs[0].set_text('Upper')
# legs[1].set_text('Middle')
# legs[2].set_text('Lower')

fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Here, in both training set and test set, the average fare closest to $80 are in the <b>C</b> Embarked values where pclass is 1. So, let's fill in the missing values as "C"

# COMMAND ----------

## Replacing the null values in the Embarked column with the mode. 
train.Embarked.fillna("C", inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Cabin Feature
# MAGIC ***

# COMMAND ----------

print("Train Cabin missing: " + str(train.Cabin.isnull().sum()/len(train.Cabin)))
print("Test Cabin missing: " + str(test.Cabin.isnull().sum()/len(test.Cabin)))

# COMMAND ----------

# MAGIC %md
# MAGIC Approximately 77% of Cabin feature is missing in the training data and 78% missing on the test data. 
# MAGIC We have two choices, 
# MAGIC * we can either get rid of the whole feature, or 
# MAGIC * we can brainstorm a little and find an appropriate way to put them in use. For example, We may say passengers with cabin record had a higher socio-economic-status then others. We may also say passengers with cabin record were more likely to be taken into consideration when loading into the boat.
# MAGIC 
# MAGIC Let's combine train and test data first and for now, will assign all the null values as **"N"**

# COMMAND ----------

## Concat train and test into a variable "all_data"
survivers = train.Survived

train.drop(["Survived"],axis=1, inplace=True)

all_data = pd.concat([train,test], ignore_index=False)

## Assign all the null values to N
all_data.Cabin.fillna("N", inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC All the cabin names start with an English alphabet following by multiple digits. It seems like there are some passengers that had booked multiple cabin rooms in their name. This is because many of them travelled with family. However, they all seem to book under the same letter followed by different numbers. It seems like there is a significance with the letters rather than the numbers. Therefore, we can group these cabins according to the letter of the cabin name.

# COMMAND ----------

all_data.Cabin = [i[0] for i in all_data.Cabin]

# COMMAND ----------

# MAGIC %md
# MAGIC Now let's look at the value counts of the cabin features and see how it looks.

# COMMAND ----------

percent_value_counts(all_data, "Cabin")

# COMMAND ----------

# MAGIC %md
# MAGIC So, We still haven't done any effective work to replace the null values. Let's stop for a second here and think through how we can take advantage of some of the other features here.  
# MAGIC * We can use the average of the fare column We can use pythons ***groupby*** function to get the mean fare of each cabin letter.

# COMMAND ----------

all_data.groupby("Cabin")['Fare'].mean().sort_values()

# COMMAND ----------

# MAGIC %md
# MAGIC Now, these means can help us determine the unknown cabins, if we compare each unknown cabin rows with the given mean's above. Let's write a simple function so that we can give cabin names based on the means.

# COMMAND ----------

def cabin_estimator(i):
    """Grouping cabin feature by the first letter"""
    a = 0
    if i<16:
        a = "G"
    elif i>=16 and i<27:
        a = "F"
    elif i>=27 and i<38:
        a = "T"
    elif i>=38 and i<47:
        a = "A"
    elif i>= 47 and i<53:
        a = "E"
    elif i>= 53 and i<54:
        a = "D"
    elif i>=54 and i<116:
        a = 'C'
    else:
        a = "B"
    return a
    

# COMMAND ----------

# MAGIC %md
# MAGIC Let's apply <b>cabin_estimator</b> function in each unknown cabins(cabin with <b>null</b> values). Once that is done we will separate our train and test to continue towards machine learning modeling.

# COMMAND ----------

with_N = all_data[all_data.Cabin == "N"]

without_N = all_data[all_data.Cabin != "N"]

# COMMAND ----------

##applying cabin estimator function. 
with_N['Cabin'] = with_N.Fare.apply(lambda x: cabin_estimator(x))

## getting back train. 
all_data = pd.concat([with_N, without_N], axis=0)

## PassengerId helps us separate train and test. 
all_data.sort_values(by = 'PassengerId', inplace=True)

## Separating train and test from all_data. 
train = all_data[:891]

test = all_data[891:]

# adding saved target variable with train. 
train['Survived'] = survivers

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fare Feature
# MAGIC ***
# MAGIC If you have paid attention so far, you know that there is only one missing value in the fare column. Let's have it.

# COMMAND ----------

test[test.Fare.isnull()]

# COMMAND ----------

# MAGIC %md
# MAGIC Here, We can take the average of the **Fare** column to fill in the NaN value. However, for the sake of learning and practicing, we will try something else. We can take the average of the values where**Pclass** is ***3***, **Sex** is ***male*** and **Embarked** is ***S***

# COMMAND ----------

missing_value = test[(test.Pclass == 3) & 
                     (test.Embarked == "S") & 
                     (test.Sex == "male")].Fare.mean()
## replace the test.fare null values with test.fare mean
test.Fare.fillna(missing_value, inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Age Feature
# MAGIC ***
# MAGIC We know that the feature "Age" is the one with most missing values, let's see it in terms of percentage.

# COMMAND ----------

print ("Train age missing value: " + str((train.Age.isnull().sum()/len(train))*100)+str("%"))
print ("Test age missing value: " + str((test.Age.isnull().sum()/len(test))*100)+str("%"))

# COMMAND ----------

# MAGIC %md
# MAGIC We will take a different approach since **~20% data in the Age column is missing** in both train and test dataset. The age variable seems to be promising for determining survival rate. Therefore, It would be unwise to replace the missing values with median, mean or mode. We will use machine learning model Random Forest Regressor to impute missing value instead of Null value. We will keep the age column unchanged for now and work on that in the feature engineering section.

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 3. Visualization and Feature Relations
# MAGIC <a id="visualization_and_feature_relations" ></a>
# MAGIC ***
# MAGIC Before we dive into finding relations between independent variables and our dependent variable(survivor), let us create some assumptions about how the relations may turn-out among features.
# MAGIC 
# MAGIC **Assumptions:**
# MAGIC - Gender: More female survived than male
# MAGIC - Pclass: Higher socio-economic status passenger survived more than others. 
# MAGIC - Age: Younger passenger survived more than other passengers. 
# MAGIC - Fare: Passenger with higher fare survived more that other passengers. This can be quite correlated with Pclass. 
# MAGIC 
# MAGIC 
# MAGIC Now, let's see how the features are related to each other by creating some visualizations.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3a. Gender and Survived
# MAGIC <a id="gender_and_survived"></a>
# MAGIC ***

# COMMAND ----------

import seaborn as sns
pal = {'male':"green", 'female':"Pink"}
sns.set(style="darkgrid")
plt.subplots(figsize = (15,8))
ax = sns.barplot(x = "Sex", 
                 y = "Survived", 
                 data=train, 
                 palette = pal,
                 linewidth=5,
                 order = ['female','male'],
                 capsize = .05,

                )

plt.title("Survived/Non-Survived Passenger Gender Distribution", fontsize = 25,loc = 'center', pad = 40)
plt.ylabel("% of passenger survived", fontsize = 15, )
plt.xlabel("Sex",fontsize = 15);



# COMMAND ----------

# MAGIC %md
# MAGIC This bar plot above shows the distribution of female and male survived. The ***x_label*** represents **Sex** feature while the ***y_label*** represents the % of **passenger survived**. This bar plot shows that ~74% female passenger survived while only ~19% male passenger survived.

# COMMAND ----------

pal = {1:"seagreen", 0:"gray"}
sns.set(style="darkgrid")
plt.subplots(figsize = (15,8))
ax = sns.countplot(x = "Sex", 
                   hue="Survived",
                   data = train, 
                   linewidth=4, 
                   palette = pal
)

## Fixing title, xlabel and ylabel
plt.title("Passenger Gender Distribution - Survived vs Not-survived", fontsize = 25, pad=40)
plt.xlabel("Sex", fontsize = 15);
plt.ylabel("# of Passenger Survived", fontsize = 15)

## Fixing xticks
#labels = ['Female', 'Male']
#plt.xticks(sorted(train.Sex.unique()), labels)

## Fixing legends
leg = ax.get_legend()
leg.set_title("Survived")
legs = leg.texts
legs[0].set_text("No")
legs[1].set_text("Yes")
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC This count plot shows the actual distribution of male and female passengers that survived and did not survive. It shows that among all the females ~ 230 survived and ~ 70 did not survive. While among male passengers ~110 survived and ~480 did not survive. 
# MAGIC 
# MAGIC **Summary**
# MAGIC ***
# MAGIC - As we suspected, female passengers have survived at a much better rate than male passengers. 
# MAGIC - It seems about right since females and children were the priority.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3b. Pclass and Survived
# MAGIC <a id="pcalss_and_survived"></a>
# MAGIC ***

# COMMAND ----------

temp = train[['Pclass', 'Survived', 'PassengerId']].groupby(['Pclass', 'Survived']).count().reset_index()
temp_df = pd.pivot_table(temp, values = 'PassengerId', index = 'Pclass',columns = 'Survived')
names = ['No', 'Yes']
temp_df.columns = names
r = [0,1,2]
totals = [i+j for i, j in zip(temp_df['No'], temp_df['Yes'])]
No_s = [i / j * 100 for i,j in zip(temp_df['No'], totals)]
Yes_s = [i / j * 100 for i,j in zip(temp_df['Yes'], totals)]
## Plotting
plt.subplots(figsize = (15,10))
barWidth = 0.60
names = ('Upper', 'Middle', 'Lower')
# Create green Bars
plt.bar(r, No_s, color='Red', edgecolor='white', width=barWidth)
# Create orange Bars
plt.bar(r, Yes_s, bottom=No_s, color='Green', edgecolor='white', width=barWidth)

 
# Custom x axis
plt.xticks(r, names)
plt.xlabel("Pclass")
plt.ylabel('Percentage')
 
# Show graphic
plt.show()


# COMMAND ----------

plt.subplots(figsize = (15,10))
sns.barplot(x = "Pclass", 
            y = "Survived", 
            data=train, 
            linewidth=6,
            capsize = .05,
            errcolor='blue',
            errwidth = 3
            

           )
plt.title("Passenger Class Distribution - Survived vs Non-Survived", fontsize = 25, pad=40)
plt.xlabel("Socio-Economic class", fontsize = 15);
plt.ylabel("% of Passenger Survived", fontsize = 15);
names = ['Upper', 'Middle', 'Lower']
#val = sorted(train.Pclass.unique())
val = [0,1,2] ## this is just a temporary trick to get the label right. 
plt.xticks(val, names);

# COMMAND ----------

# MAGIC %md
# MAGIC - It looks like ...
# MAGIC     - ~ 63% first class passenger survived titanic tragedy, while 
# MAGIC     - ~ 48% second class and 
# MAGIC     - ~ only  24% third class passenger survived.

# COMMAND ----------

# Kernel Density Plot
fig = plt.figure(figsize=(15,8),)
## I have included to different ways to code a plot below, choose the one that suites you. 
ax=sns.kdeplot(train.Pclass[train.Survived == 0] , 
               color='gray',
               shade=True,
               label='not survived')
ax=sns.kdeplot(train.loc[(train['Survived'] == 1),'Pclass'] , 
               color='g',
               shade=True, 
               label='survived', 
              )
plt.title('Passenger Class Distribution - Survived vs Non-Survived', fontsize = 25, pad = 40)
plt.ylabel("Frequency of Passenger Survived", fontsize = 15, labelpad = 20)
plt.xlabel("Passenger Class", fontsize = 15,labelpad =20)
## Converting xticks into words for better understanding
labels = ['Upper', 'Middle', 'Lower']
plt.xticks(sorted(train.Pclass.unique()), labels);

# COMMAND ----------

# MAGIC %md
# MAGIC This KDE plot is pretty self-explanatory with all the labels and colors. Something I have noticed that some readers might find questionable is that the lower class passengers have survived more than second-class passengers. It is true since there were a lot more third-class passengers than first and second. 
# MAGIC 
# MAGIC **Summary**
# MAGIC ***
# MAGIC The first class passengers had the upper hand during the tragedy. You can probably agree with me more on this, in the next section of visualizations where we look at the distribution of ticket fare and survived column.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3c. Fare and Survived
# MAGIC <a id="fare_and_survived"></a>
# MAGIC ***

# COMMAND ----------

# Kernel Density Plot
fig = plt.figure(figsize=(15,8),)
ax=sns.kdeplot(train.loc[(train['Survived'] == 0),'Fare'] , color='gray',shade=True,label='not survived')
ax=sns.kdeplot(train.loc[(train['Survived'] == 1),'Fare'] , color='g',shade=True, label='survived')
plt.title('Fare Distribution Survived vs Non Survived', fontsize = 25, pad = 40)
plt.ylabel("Frequency of Passenger Survived", fontsize = 15, labelpad = 20)
plt.xlabel("Fare", fontsize = 15, labelpad = 20);



# COMMAND ----------

# MAGIC %md
# MAGIC This plot shows something impressive..
# MAGIC - The spike in the plot under 100 dollar represents that a lot of passengers who bought the ticket within that range did not survive. 
# MAGIC - When fare is approximately more than 280 dollars, there is no gray shade which means, either everyone passed that fare point survived or maybe there is an outlier that clouds our judgment. Let's check...

# COMMAND ----------

train[train.Fare > 280]

# COMMAND ----------

# MAGIC %md
# MAGIC As we assumed, it looks like an outlier with a fare of $512. We sure can delete this point. However, we will keep it for now.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3d. Age and Survived
# MAGIC <a id="age_and_survived"></a>
# MAGIC ***

# COMMAND ----------

# Kernel Density Plot
fig = plt.figure(figsize=(15,8),)
ax=sns.kdeplot(train.loc[(train['Survived'] == 0),'Age'] , color='gray',shade=True,label='not survived')
ax=sns.kdeplot(train.loc[(train['Survived'] == 1),'Age'] , color='g',shade=True, label='survived')
plt.title('Age Distribution - Surviver V.S. Non Survivors', fontsize = 25, pad = 40)
plt.xlabel("Age", fontsize = 15, labelpad = 20)
plt.ylabel('Frequency', fontsize = 15, labelpad= 20);

# COMMAND ----------

# MAGIC %md
# MAGIC There is nothing out of the ordinary about this plot, except the very left part of the distribution. This may hint on the posibility that children and infants were the priority.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3e. Combined Feature Relations
# MAGIC <a id='combined_feature_relations'></a>
# MAGIC ***
# MAGIC In this section, we are going to discover more than two feature relations in a single graph. I will try my best to illustrate most of the feature relations. Let's get to it.

# COMMAND ----------

pal = {1:"seagreen", 0:"gray"}
g = sns.FacetGrid(train,size=5, col="Sex", row="Survived", margin_titles=True, hue = "Survived",
                  palette=pal)
g = g.map(plt.hist, "Age", edgecolor = 'white');
g.fig.suptitle("Survived by Sex and Age", size = 25)
plt.subplots_adjust(top=0.90)


# COMMAND ----------

# MAGIC %md
# MAGIC Facetgrid is a great way to visualize multiple variables and their relationships at once. From the chart in section 3a we have a intuation that female passengers had better prority than males during the tragedy. However, from this facet grid, we can also understand which age range groups survived more than others or were not so lucky

# COMMAND ----------

g = sns.FacetGrid(train,size=5, col="Sex", row="Embarked", margin_titles=True, hue = "Survived",
                  palette = pal
                  )
g = g.map(plt.hist, "Age", edgecolor = 'white').add_legend();
g.fig.suptitle("Survived by Sex and Age", size = 25)
plt.subplots_adjust(top=0.90)

# COMMAND ----------

# MAGIC %md
# MAGIC This is another compelling facet grid illustrating four features relationship at once. They are **Embarked, Age, Survived & Sex**. 
# MAGIC * The color illustrates passengers survival status(green represents survived, gray represents not survived)
# MAGIC * The column represents Sex(left being male, right stands for female)
# MAGIC * The row represents Embarked(from top to bottom: S, C, Q)
# MAGIC ***
# MAGIC Now that I have steered out the apparent let's see if we can get some insights that are not so obvious as we look at the data. 
# MAGIC * Most passengers seem to be boarded on Southampton(S).
# MAGIC * More than 60% of the passengers died boarded on Southampton. 
# MAGIC * More than 60% of the passengers lived boarded on Cherbourg(C).
# MAGIC * Pretty much every male that boarded on Queenstown(Q) did not survive. 
# MAGIC * There were very few females boarded on Queenstown, however, most of them survived.

# COMMAND ----------

g = sns.FacetGrid(train, size=5,hue="Survived", col ="Sex", margin_titles=True,
                palette=pal,)
g.map(plt.scatter, "Fare", "Age",edgecolor="w").add_legend()
g.fig.suptitle("Survived by Sex, Fare and Age", size = 25)
plt.subplots_adjust(top=0.85)

# COMMAND ----------

# MAGIC %md
# MAGIC This facet grid unveils a couple of interesting insights. Let's find out.
# MAGIC * The grid above clearly demonstrates the three outliers with Fare of over \$500. At this point, I think we are quite confident that these outliers should be deleted.
# MAGIC * Most of the passengers were with in the Fare range of \$100.

# COMMAND ----------

## dropping the three outliers where Fare is over $500 
train = train[train.Fare < 500]
## factor plot
sns.factorplot(x = "Parch", y = "Survived", data = train,kind = "point",size = 8)
plt.title("Factorplot of Parents/Children survived", fontsize = 25)
plt.subplots_adjust(top=0.85)

# COMMAND ----------

# MAGIC %md
# MAGIC **Passenger who traveled in big groups with parents/children had less survival rate than other passengers.**

# COMMAND ----------

sns.factorplot(x =  "SibSp", y = "Survived", data = train,kind = "point",size = 8)
plt.title('Factorplot of Sibilings/Spouses survived', fontsize = 25)
plt.subplots_adjust(top=0.85)

# COMMAND ----------

# MAGIC %md
# MAGIC **While, passenger who traveled in small groups with sibilings/spouses had better changes of survivint than other passengers.**

# COMMAND ----------

# Placing 0 for female and 
# 1 for male in the "Sex" column. 
train['Sex'] = train.Sex.apply(lambda x: 0 if x == "female" else 1)
test['Sex'] = test.Sex.apply(lambda x: 0 if x == "female" else 1)

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 4: Statistical Overview
# MAGIC <a id="statisticaloverview"></a>
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC ![title](https://cdn-images-1.medium.com/max/400/1*hFJ-LI7IXcWpxSLtaC0dfg.png)

# COMMAND ----------

# MAGIC %md
# MAGIC **Train info**

# COMMAND ----------

train.describe()

# COMMAND ----------

train.describe(include =['O'])

# COMMAND ----------

# Overview(Survived vs non survied)
survived_summary = train.groupby("Survived")
survived_summary.mean().reset_index()

# COMMAND ----------

survived_summary = train.groupby("Sex")
survived_summary.mean().reset_index()

# COMMAND ----------

survived_summary = train.groupby("Pclass")
survived_summary.mean().reset_index()

# COMMAND ----------

# MAGIC %md
# MAGIC I have gathered a small summary from the statistical overview above. Let's see what they are...
# MAGIC - This train data set has 891 raw and 9 columns. 
# MAGIC - only 38% passenger survived during that tragedy.
# MAGIC - ~74% female passenger survived, while only ~19% male passenger survived. 
# MAGIC - ~63% first class passengers survived, while only 24% lower class passenger survived.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4a. Correlation Matrix and Heatmap
# MAGIC <a id="heatmap"></a>
# MAGIC ***
# MAGIC ### Correlations

# COMMAND ----------

pd.DataFrame(abs(train.corr()['Survived']).sort_values(ascending = False))

# COMMAND ----------

# MAGIC %md
# MAGIC ** Sex is the most important correlated feature with *Survived(dependent variable)* feature followed by Pclass.**

# COMMAND ----------

## get the most important variables. 
corr = train.corr()**2
corr.Survived.sort_values(ascending=False)

# COMMAND ----------

# MAGIC %md
# MAGIC **Squaring the correlation feature not only gives on positive correlations but also amplifies the relationships.**

# COMMAND ----------

## heatmeap to see the correlation between features. 
# Generate a mask for the upper triangle (taken from seaborn example gallery)
import numpy as np
mask = np.zeros_like(train.corr(), dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
sns.set_style('whitegrid')
plt.subplots(figsize = (15,12))
sns.heatmap(train.corr(), 
            annot=True,
            mask = mask,
            cmap = 'RdBu', ## in order to reverse the bar replace "RdBu" with "RdBu_r"
            linewidths=.9, 
            linecolor='white',
            fmt='.2g',
            center = 0,
            square=True)
plt.title("Correlations Among Features", y = 1.03,fontsize = 20, pad = 40);

# COMMAND ----------

# MAGIC %md
# MAGIC #### Positive Correlation Features:
# MAGIC - Fare and Survived: 0.26
# MAGIC 
# MAGIC #### Negative Correlation Features:
# MAGIC - Fare and Pclass: -0.6
# MAGIC - Sex and Survived: -0.55
# MAGIC - Pclass and Survived: -0.33
# MAGIC 
# MAGIC 
# MAGIC **So, Let's analyze these correlations a bit.** We have found some moderately strong relationships between different features. There is a definite positive correlation between Fare and Survived rated. This relationship reveals that the passenger who paid more money for their ticket were more likely to survive. This theory aligns with one other correlation which is the correlation between Fare and Pclass(-0.6). This relationship can be explained by saying that first class passenger(1) paid more for fare then second class passenger(2), similarly second class passenger paid more than the third class passenger(3). This theory can also be supported by mentioning another Pclass correlation with our dependent variable, Survived. The correlation between Pclass and Survived is -0.33. This can also be explained by saying that first class passenger had a better chance of surviving than the second or the third and so on.
# MAGIC 
# MAGIC However, the most significant correlation with our dependent variable is the Sex variable, which is the info on whether the passenger was male or female. This negative correlation with a magnitude of -0.54 which points towards some undeniable insights. Let's do some statistics to see how statistically significant this correlation is.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4b. Statistical Test for Correlation
# MAGIC <a id="statistical_test"></a>
# MAGIC ***
# MAGIC 
# MAGIC Statistical tests are the scientific way to prove the validation of theories. In any case, when we look at the data, we seem to have an intuitive understanding of where data is leading us. However, when we do statistical tests, we get a scientific or mathematical perspective of how significant these results are. Let's apply some of these methods and see how we are doing with our predictions.
# MAGIC 
# MAGIC ###  Hypothesis Testing Outline
# MAGIC 
# MAGIC A hypothesis test compares the mean of a control group and experimental group and tries to find out whether the two sample means are different from each other and if they are different, how significant that difference is.
# MAGIC  
# MAGIC A **hypothesis test** usually consists of multiple parts: 
# MAGIC 
# MAGIC 1. Formulate a well-developed research problem or question: The hypothesis test usually starts with a concrete and well-developed researched problem. We need to ask the right question that can be answered using statistical analysis. 
# MAGIC 2. **The null hypothesis($H_0$) and Alternating hypothesis($H_1$)**:
# MAGIC > * The **null hypothesis($H_0$)** is something that is assumed to be true. It is the status quo. In a null hypothesis, the observations are the result of pure chance. When we set out to experiment, we form the null hypothesis by saying that there is no difference between the means of the control group and the experimental group.
# MAGIC > *  An **Alternative hypothesis($H_A$)** is a claim and the opposite of the null hypothesis.  It is going against the status quo. In an alternative theory, the observations show a real effect combined with a component of chance variation.
# MAGIC     
# MAGIC 3. Determine the **test statistic**: test statistic can be used to assess the truth of the null hypothesis. Depending on the standard deviation we either use t-statistics or z-statistics. In addition to that, we want to identify whether the test is a one-tailed test or two-tailed test. [This](https://support.minitab.com/en-us/minitab/18/help-and-how-to/statistics/basic-statistics/supporting-topics/basics/null-and-alternative-hypotheses/) article explains it pretty well. [This](https://stattrek.com/hypothesis-test/hypothesis-testing.aspx) article is pretty good as well. 
# MAGIC 
# MAGIC 4. Specify a **Significance level** and **Confidence Interval**: The significance level($\alpha$) is the probability of rejecting a null hypothesis when it is true. In other words, we are ***comfortable/confident*** with rejecting the null hypothesis a significant amount of times even though it is true. This considerable amount is our Significant level. In addition to that, Significance level is one minus our Confidence interval. For example, if we say, our significance level is 5%, then our confidence interval would be (1 - 0.05) = 0.95 or 95%. 
# MAGIC 
# MAGIC 5. Compute the **T-Statistics/Z-Statistics**: Computing the t-statistics follows a simple equation. This equation slightly differs depending on one sample test or two sample test  
# MAGIC 
# MAGIC 6. Compute the **P-value**: P-value is the probability that a test statistic at least as significant as the one observed would be obtained assuming that the null hypothesis is correct. The p-value is known to be unintuitive, and even many professors are known to explain it wrong. I think this [video](https://www.youtube.com/watch?v=E4KCfcVwzyw) explains the p-value well. **The smaller the P-value, the stronger the evidence against the null hypothesis.**
# MAGIC 
# MAGIC 7. **Describe the result and compare the p-value with the significance value($\alpha$)**: If p<=$\alpha$, then the observed effect is statistically significant, the null hypothesis is ruled out, and the alternative hypothesis is valid. However if the p> $\alpha$, we say that, we fail to reject the null hypothesis. Even though this sentence is grammatically wrong, it is logically right. We never accept the null hypothesis just because we are doing the statistical test with sample data points.
# MAGIC 
# MAGIC We will follow each of these steps above to do your hypothesis testing below.
# MAGIC 
# MAGIC P.S. Khan Academy has a set of videos that I think are intuative and helped me understand conceptually. 
# MAGIC 
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC ### Hypothesis testing for Titanic
# MAGIC #### Formulating a well developed researched question: 
# MAGIC Regarding this dataset, we can formulate the null hypothesis and alternative hypothesis by asking the following questions. 
# MAGIC > * **Is there a significant difference in the mean sex between the passenger who survived and passenger who did not survive?**. 
# MAGIC > * **Is there a substantial difference in the survival rate between the male and female passengers?**
# MAGIC 
# MAGIC 
# MAGIC #### The Null Hypothesis and The Alternative Hypothesis:
# MAGIC We can formulate our hypothesis by asking questions differently. However, it is essential to understand what our end goal is. Here our dependent variable or target variable is **Survived**. Therefore, we say
# MAGIC 
# MAGIC > ** Null Hypothesis($H_0$):** There is no difference in the survival rate between the male and female passengers. or the mean difference between male and female passenger in the survival rate is zero.  
# MAGIC >  ** Alternative Hypothesis($H_A$):** There is a difference in the survival rate between the male and female passengers. or the mean difference in the survival rate between male and female is not zero.
# MAGIC 
# MAGIC 
# MAGIC Onc thing we can do is try to set up the Null and Alternative Hypothesis in such way that, when we do our t-test, we can choose to do one tailed test. According to [this](https://support.minitab.com/en-us/minitab/18/help-and-how-to/statistics/basic-statistics/supporting-topics/basics/null-and-alternative-hypotheses/) article, one-tailed tests are more powerful than two-tailed test. In addition to that, [this](https://www.youtube.com/watch?v=5NcMFlrnYp8&list=PLIeGtxpvyG-LrjxQ60pxZaimkaKKs0zGF) video is also quite helpful understanding these topics. with this in mind we can update/modify our null and alternative hypothesis. Let's see how we can rewrite this..
# MAGIC 
# MAGIC > **Null Hypothesis(H0):** male mean is greater or equal to female mean.
# MAGIC 
# MAGIC > **Alternative Hypothesis(H1):** male mean is less than female mean. 
# MAGIC 
# MAGIC #### Determine the test statistics:
# MAGIC > This will be a two-tailed test since the difference between male and female passenger in the survival rate could be higher or lower than 0. 
# MAGIC > Since we do not know the standard deviation($\sigma$) and n is small, we will use the t-distribution. 
# MAGIC 
# MAGIC #### Specify the significance level:
# MAGIC > Specifying a significance level is an important step of the hypothesis test. It is an ultimate balance between type 1 error and type 2 error. We will discuss more in-depth about those in another lesson. For now, we have decided to make our significance level($\alpha$) = 0.05. So, our confidence interval or non-rejection region would be (1 - $\alpha$)=(1-0.05) = 95%. 
# MAGIC 
# MAGIC #### Computing T-statistics and P-value:
# MAGIC Let's take a random sample and see the difference.

# COMMAND ----------

male_mean = train[train['Sex'] == 1].Survived.mean()

female_mean = train[train['Sex'] == 0].Survived.mean()
print ("Male survival mean: " + str(male_mean))
print ("female survival mean: " + str(female_mean))

print ("The mean difference between male and female survival rate: " + str(female_mean - male_mean))

# COMMAND ----------

# MAGIC %md
# MAGIC Now, we have to understand that those two means are not  **the population mean ($\bar{\mu}$)**.  *The population mean is a statistical term statistician uses to indicate the actual average of the entire group. The group can be any gathering of multiple numbers such as animal, human, plants, money, stocks.* For example, To find the age population mean of Bulgaria; we will have to account for every single person's age and take their age. Which is almost impossible and if we were to go that route; there is no point of doing statistics in the first place. Therefore we approach this problem using sample sets. The idea of using sample set is that; if we take multiple samples of the same population and take the mean of them and put them in a distribution; eventually the distribution start to look more like a **normal distribution**. The more samples we take and the more sample means will be added and, the closer the normal distribution will reach towards population mean. This is where **Central limit theory** comes from. We will go more in depth of this topic later on. 
# MAGIC 
# MAGIC Going back to our dataset, like we are saying these means above are part of the whole story. We were given part of the data to train our machine learning models, and the other part of the data was held back for testing. Therefore, It is impossible for us at this point to know the population means of survival for male and females. Situation like this calls for a statistical approach. We will use the sampling distribution approach to do the test. let's take 50 random sample of male and female from our train data.

# COMMAND ----------

# separating male and female dataframe. 
import random
male = train[train['Sex'] == 1]
female = train[train['Sex'] == 0]

## empty list for storing mean sample
m_mean_samples = []
f_mean_samples = []

for i in range(50):
    m_mean_samples.append(np.mean(random.sample(list(male['Survived']),50,)))
    f_mean_samples.append(np.mean(random.sample(list(female['Survived']),50,)))
    

# Print them out
print (f"Male mean sample mean: {round(np.mean(m_mean_samples),2)}")
print (f"Male mean sample mean: {round(np.mean(f_mean_samples),2)}")
print (f"Difference between male and female mean sample mean: {round(np.mean(f_mean_samples) - np.mean(m_mean_samples),2)}")

# COMMAND ----------

# MAGIC %md
# MAGIC H0: male mean is greater or equal to female mean<br>
# MAGIC H1: male mean is less than female mean.

# COMMAND ----------

# MAGIC %md
# MAGIC According to the samples our male samples ($\bar{x}_m$) and female samples($\bar{x}_f$) mean measured difference is ~ 0.55(statistically this is called the point estimate of the male population mean and female population mean). keeping in mind that...
# MAGIC * We randomly select 50 people to be in the male group and 50 people to be in the female group. 
# MAGIC * We know our sample is selected from a broader population(trainning set). 
# MAGIC * We know we could have totally ended up with a different random sample of males and females.
# MAGIC ***
# MAGIC With all three points above in mind, how confident are we that, the measured difference is real or statistically significant? we can perform a **t-test** to evaluate that. When we perform a **t-test** we are usually trying to find out **an evidence of significant difference between population mean with hypothesized mean(1 sample t-test) or in our case difference between two population means(2 sample t-test).** 
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC The **t-statistics** is the measure of a degree to which our groups differ standardized by the variance of our measurements. In order words, it is basically the measure of signal over noise. Let us describe the previous sentence a bit more for clarification. I am going to use [this post](http://blog.minitab.com/blog/statistics-and-quality-data-analysis/what-is-a-t-test-and-why-is-it-like-telling-a-kid-to-clean-up-that-mess-in-the-kitchen) as reference to describe the t-statistics here. 
# MAGIC 
# MAGIC 
# MAGIC #### Calculating the t-statistics
# MAGIC # $$t = \frac{\bar{x}-\mu}{\frac{S} {\sqrt{n}} }$$
# MAGIC 
# MAGIC Here..
# MAGIC * $\bar{x}$ is the sample mean. 
# MAGIC * $\mu$ is the hypothesized mean. 
# MAGIC * S is the standard deviation. 
# MAGIC * n is the sample size. 
# MAGIC 
# MAGIC 
# MAGIC 1. Now, the denominator of this fraction $(\bar{x}-\mu)$ is basically the strength of the signal. where we calculate the difference between hypothesized mean and sample mean. If the mean difference is higher, then the signal is stronger. 
# MAGIC 
# MAGIC the numerator of this fraction ** ${S}/ {\sqrt{n}}$ ** calculates the amount of variation or noise of the data set. Here S is standard deviation, which tells us how much variation is there in the data. n is the sample size. 
# MAGIC 
# MAGIC So, according to the explanation above, the t-value or t-statistics is basically measures the strength of the signal(the difference) to the amount of noise(the variation) in the data and that is how we calculate the t-value in one sample t-test. However, in order to calculate between two sample population mean or in our case we will use the follow equation. 
# MAGIC 
# MAGIC # $$t = \frac{\bar{x}_M - \bar{x}_F}{\sqrt {s^2 (\frac{1}{n_M} + \frac{1}{n_F})}}$$
# MAGIC 
# MAGIC This equation may seem too complex, however, the idea behind these two are similar. Both of them have the concept of signal/noise. The only difference is that we replace our hypothesis mean with another sample mean and the two sample sizes repalce one sample size. 
# MAGIC 
# MAGIC Here..
# MAGIC * $\bar{x}_M$ is the mean of our male group sample measurements. 
# MAGIC * $ \bar{x}_F$ is the mean of female group samples. 
# MAGIC * $ n_M$ and $n_F$ are the sample number of observations in each group. 
# MAGIC * $ S^2$ is the sample variance.
# MAGIC 
# MAGIC It is good to have an understanding of what going on in the background. However, we will use **scipy.stats** to find the t-statistics.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Compare P-value with $\alpha$
# MAGIC > It looks like the p-value is very small compared to our significance level($\alpha$)of 0.05. Our observation sample is statistically significant. Therefore, our null hypothesis is ruled out, and our alternative hypothesis is valid, which is "**There is a significant difference in the survival rate between the male and female passengers."**

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 5: Feature Engineering
# MAGIC <a id="feature_engineering"></a>
# MAGIC ***
# MAGIC Feature Engineering is exactly what its sounds like. Sometimes we want to create extra features from with in the features that we have, sometimes we want to remove features that are alike. Features engineering is the simple word for doing all those. It is important to remember that we will create new features in such ways that will not cause **multicollinearity(when there is a relationship among independent variables)** to occur.

# COMMAND ----------

# MAGIC %md
# MAGIC ## name_length
# MAGIC ***Creating a new feature "name_length" that will take the count of letters of each name***

# COMMAND ----------

# Creating a new colomn with a 
train['name_length'] = [len(i) for i in train.Name]
test['name_length'] = [len(i) for i in test.Name]

def name_length_group(size):
    a = ''
    if (size <=20):
        a = 'short'
    elif (size <=35):
        a = 'medium'
    elif (size <=45):
        a = 'good'
    else:
        a = 'long'
    return a


train['nLength_group'] = train['name_length'].map(name_length_group)
test['nLength_group'] = test['name_length'].map(name_length_group)

## Here "map" is python's built-in function. 
## "map" function basically takes a function and 
## returns an iterable list/tuple or in this case series. 
## However,"map" can also be used like map(function) e.g. map(name_length_group) 
## or map(function, iterable{list, tuple}) e.g. map(name_length_group, train[feature]]). 
## However, here we don't need to use parameter("size") for name_length_group because when we 
## used the map function like ".map" with a series before dot, we are basically hinting that series 
## and the iterable. This is similar to .append approach in python. list.append(a) meaning applying append on list. 


## cuts the column by given bins based on the range of name_length
#group_names = ['short', 'medium', 'good', 'long']
#train['name_len_group'] = pd.cut(train['name_length'], bins = 4, labels=group_names)

# COMMAND ----------

# MAGIC %md
# MAGIC ## title
# MAGIC **Getting the title of each name as a new feature. **

# COMMAND ----------

## get the title from the name
train["title"] = [i.split('.')[0] for i in train.Name]
train["title"] = [i.split(',')[1] for i in train.title]
## Whenever we split like that, there is a good change that we will end up with while space around our string values. Let's check that. 

# COMMAND ----------

print(train.title.unique())

# COMMAND ----------

## Let's fix that
train.title = train.title.apply(lambda x: x.strip())

# COMMAND ----------

## We can also combile all three lines above for test set here
test['title'] = [i.split('.')[0].split(',')[1].strip() for i in test.Name]

## However it is important to be able to write readable code, and the line above is not so readable. 

# COMMAND ----------

## Let's replace some of the rare values with the keyword 'rare' and other word choice of our own. 
## train Data
train["title"] = [i.replace('Ms', 'Miss') for i in train.title]
train["title"] = [i.replace('Mlle', 'Miss') for i in train.title]
train["title"] = [i.replace('Mme', 'Mrs') for i in train.title]
train["title"] = [i.replace('Dr', 'rare') for i in train.title]
train["title"] = [i.replace('Col', 'rare') for i in train.title]
train["title"] = [i.replace('Major', 'rare') for i in train.title]
train["title"] = [i.replace('Don', 'rare') for i in train.title]
train["title"] = [i.replace('Jonkheer', 'rare') for i in train.title]
train["title"] = [i.replace('Sir', 'rare') for i in train.title]
train["title"] = [i.replace('Lady', 'rare') for i in train.title]
train["title"] = [i.replace('Capt', 'rare') for i in train.title]
train["title"] = [i.replace('the Countess', 'rare') for i in train.title]
train["title"] = [i.replace('Rev', 'rare') for i in train.title]


## Now in programming there is a term called DRY(Don't repeat yourself), whenever we are repeating  
## same code over and over again, there should be a light-bulb turning on in our head and make us think
## to code in a way that is not repeating or dull. Let's write a function to do exactly what we 
## did in the code above, only not repeating and more interesting. 

# COMMAND ----------

## we are writing a function that can help us modify title column
def name_converted(feature):
    """
    This function helps modifying the title column
    """
    
    result = ''
    if feature in ['the Countess','Capt','Lady','Sir','Jonkheer','Don','Major','Col', 'Rev', 'Dona', 'Dr']:
        result = 'rare'
    elif feature in ['Ms', 'Mlle']:
        result = 'Miss'
    elif feature == 'Mme':
        result = 'Mrs'
    else:
        result = feature
    return result

test.title = test.title.map(name_converted)
train.title = train.title.map(name_converted)

# COMMAND ----------

print(train.title.unique())
print(test.title.unique())

# COMMAND ----------

# MAGIC %md
# MAGIC ## family_size
# MAGIC ***Creating a new feature called "family_size".***

# COMMAND ----------

## Family_size seems like a good feature to create
train['family_size'] = train.SibSp + train.Parch+1
test['family_size'] = test.SibSp + test.Parch+1

# COMMAND ----------

## bin the family size. 
def family_group(size):
    """
    This funciton groups(loner, small, large) family based on family size
    """
    
    a = ''
    if (size <= 1):
        a = 'loner'
    elif (size <= 4):
        a = 'small'
    else:
        a = 'large'
    return a

# COMMAND ----------

## apply the family_group function in family_size
train['family_group'] = train['family_size'].map(family_group)
test['family_group'] = test['family_size'].map(family_group)

# COMMAND ----------

# MAGIC %md
# MAGIC ## is_alone

# COMMAND ----------

train['is_alone'] = [1 if i<2 else 0 for i in train.family_size]
test['is_alone'] = [1 if i<2 else 0 for i in test.family_size]

# COMMAND ----------

# MAGIC %md
# MAGIC ## ticket

# COMMAND ----------

train.Ticket.value_counts().sample(10)

# COMMAND ----------

# MAGIC %md
# MAGIC I have yet to figureout how to best manage ticket feature. So, any suggestion would be truly appreciated. For now, I will get rid off the ticket feature.

# COMMAND ----------

train.drop(['Ticket'], axis=1, inplace=True)

test.drop(['Ticket'], axis=1, inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## calculated_fare

# COMMAND ----------

## Calculating fare based on family size. 
train['calculated_fare'] = train.Fare/train.family_size
test['calculated_fare'] = test.Fare/test.family_size

# COMMAND ----------

# MAGIC %md
# MAGIC Some people have travelled in groups like family or friends. It seems like Fare column kept a record of the total fare rather than the fare of individual passenger, therefore calculated fare will be much handy in this situation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## fare_group

# COMMAND ----------

def fare_group(fare):
    """
    This function creates a fare group based on the fare provided
    """
    
    a= ''
    if fare <= 4:
        a = 'Very_low'
    elif fare <= 10:
        a = 'low'
    elif fare <= 20:
        a = 'mid'
    elif fare <= 45:
        a = 'high'
    else:
        a = "very_high"
    return a

train['fare_group'] = train['calculated_fare'].map(fare_group)
test['fare_group'] = test['calculated_fare'].map(fare_group)

#train['fare_group'] = pd.cut(train['calculated_fare'], bins = 4, labels=groups)

# COMMAND ----------

# MAGIC %md
# MAGIC Fare group was calculated based on <i>calculated_fare</i>. This can further help our cause.

# COMMAND ----------

# MAGIC %md
# MAGIC ## PassengerId

# COMMAND ----------

# MAGIC %md
# MAGIC It seems like <i>PassengerId</i> column only works as an id in this dataset without any significant effect on the dataset. Let's drop it.

# COMMAND ----------

train.drop(['PassengerId'], axis=1, inplace=True)

test.drop(['PassengerId'], axis=1, inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating dummy variables
# MAGIC 
# MAGIC You might be wondering what is a dummy variable? 
# MAGIC 
# MAGIC Dummy variable is an important **prepocessing machine learning step**. Often times Categorical variables are an important features, which can be the difference between a good model and a great model. While working with a dataset, having meaningful value for example, "male" or "female" instead of 0's and 1's is more intuitive for us. However, machines do not understand the value of categorical values, for example, in this dataset we have gender male or female, algorithms do not accept categorical variables as input. In order to feed data in a machine learning model, we

# COMMAND ----------


train = pd.get_dummies(train, columns=['title',"Pclass", 'Cabin','Embarked','nLength_group', 'family_group', 'fare_group'], drop_first=False)
test = pd.get_dummies(test, columns=['title',"Pclass",'Cabin','Embarked','nLength_group', 'family_group', 'fare_group'], drop_first=False)
train.drop(['family_size','Name', 'Fare','name_length'], axis=1, inplace=True)
test.drop(['Name','family_size',"Fare",'name_length'], axis=1, inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## age

# COMMAND ----------

# MAGIC %md
# MAGIC As I promised before, we are going to use Random forest regressor in this section to predict the missing age values. Let's do it

# COMMAND ----------

train.head()

# COMMAND ----------

## rearranging the columns so that I can easily use the dataframe to predict the missing age values. 
train = pd.concat([train[["Survived", "Age", "Sex","SibSp","Parch"]], train.loc[:,"is_alone":]], axis=1)
test = pd.concat([test[["Age", "Sex"]], test.loc[:,"SibSp":]], axis=1)

# COMMAND ----------

## Importing RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

## writing a function that takes a dataframe with missing values and outputs it by filling the missing values. 
def completing_age(df):
    ## gettting all the features except survived
    age_df = df.loc[:,"Age":] 
    
    temp_train = age_df.loc[age_df.Age.notnull()] ## df with age values
    temp_test = age_df.loc[age_df.Age.isnull()] ## df without age values
    
    y = temp_train.Age.values ## setting target variables(age) in y 
    x = temp_train.loc[:, "Sex":].values
    
    rfr = RandomForestRegressor(n_estimators=1500, n_jobs=-1)
    rfr.fit(x, y)
    
    predicted_age = rfr.predict(temp_test.loc[:, "Sex":])
    
    df.loc[df.Age.isnull(), "Age"] = predicted_age
    

    return df

## Implementing the completing_age function in both train and test dataset. 
completing_age(train)
completing_age(test);

# COMMAND ----------

# MAGIC %md
# MAGIC Let's take a look at the histogram of the age column.

# COMMAND ----------

## Let's look at the his
plt.subplots(figsize = (22,10),)
sns.distplot(train.Age, bins = 100, kde = True, rug = False, norm_hist=False);

# COMMAND ----------

# MAGIC %md
# MAGIC ## age_group
# MAGIC We can create a new feature by grouping the "Age" column

# COMMAND ----------

## create bins for age
def age_group_fun(age):
    """
    This function creates a bin for age
    """
    a = ''
    if age <= 1:
        a = 'infant'
    elif age <= 4: 
        a = 'toddler'
    elif age <= 13:
        a = 'child'
    elif age <= 18:
        a = 'teenager'
    elif age <= 35:
        a = 'Young_Adult'
    elif age <= 45:
        a = 'adult'
    elif age <= 55:
        a = 'middle_aged'
    elif age <= 65:
        a = 'senior_citizen'
    else:
        a = 'old'
    return a
        
## Applying "age_group_fun" function to the "Age" column.
train['age_group'] = train['Age'].map(age_group_fun)
test['age_group'] = test['Age'].map(age_group_fun)

## Creating dummies for "age_group" feature. 
train = pd.get_dummies(train,columns=['age_group'], drop_first=True)
test = pd.get_dummies(test,columns=['age_group'], drop_first=True);

# COMMAND ----------

# MAGIC %md
# MAGIC <div class="alert alert-danger">
# MAGIC <h1>Need to paraphrase this section</h1>
# MAGIC <h2>Feature Selection</h2>
# MAGIC <h3>Feature selection is an important part of machine learning models. There are many reasons why we use feature selection.</h3> 
# MAGIC <ul>
# MAGIC     <li>Simple models are easier to interpret. People who acts according to model results have a better understanding of the model.</li>
# MAGIC     <li>Shorter training times.</li>
# MAGIC     <li>Enhanced generalisation by reducing overfitting. </li>
# MAGIC     <li>Easier to implement by software developers> model production.</li>
# MAGIC         <ul>
# MAGIC             <li>As Data Scientists we need to remember no to creating models with too many variables since it might overwhelm production engineers.</li>
# MAGIC     </ul>
# MAGIC     <li>Reduced risk of data errors during model use</li>
# MAGIC     <li>Data redundancy</li>
# MAGIC </ul>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 6: Pre-Modeling Tasks
# MAGIC ## 6a. Separating dependent and independent variables
# MAGIC <a id="dependent_independent"></a>
# MAGIC ***
# MAGIC Before we apply any machine learning models, It is important to separate dependent and independent variables. Our dependent variable or target variable is something that we are trying to find, and our independent variable is the features we use to find the dependent variable. The way we use machine learning algorithm in a dataset is that we train our machine learning model by specifying independent variables and dependent variable. To specify them, we need to separate them from each other, and the code below does just that.
# MAGIC 
# MAGIC P.S. In our test dataset, we do not have a dependent variable feature. We are to predict that using machine learning models.

# COMMAND ----------

# separating our independent and dependent variable
X = train.drop(['Survived'], axis = 1)
y = train["Survived"]

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6b. Splitting the training data
# MAGIC <a id="split_training_data" ></a>
# MAGIC ***
# MAGIC There are multiple ways of splitting data. They are...
# MAGIC * train_test_split.
# MAGIC * cross_validation. 
# MAGIC 
# MAGIC We have separated dependent and independent features; We have separated train and test data. So, why do we still have to split our training data? If you are curious about that, I have the answer. For this competition, when we train the machine learning algorithms, we use part of the training set usually two-thirds of the train data. Once we train our algorithm using 2/3 of the train data, we start to test our algorithms using the remaining data. If the model performs well we dump our test data in the algorithms to predict and submit the competition. The code below, basically splits the train data into 4 parts, **X_train**, **X_test**, **y_train**, **y_test**.  
# MAGIC * **X_train** and **y_train** first used to train the algorithm. 
# MAGIC * then, **X_test** is used in that trained algorithms to predict **outcomes. **
# MAGIC * Once we get the **outcomes**, we compare it with **y_test**
# MAGIC 
# MAGIC By comparing the **outcome** of the model with **y_test**, we can determine whether our algorithms are performing well or not. As we compare we use confusion matrix to determine different aspects of model performance.
# MAGIC 
# MAGIC P.S. When we use cross validation it is important to remember not to use **X_train, X_test, y_train and y_test**, rather we will use **X and y**. I will discuss more on that.

# COMMAND ----------

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = .33, random_state=0)

# COMMAND ----------

len(X_train)

# COMMAND ----------

len(X_test)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6c. Feature Scaling
# MAGIC <a id="feature_scaling" ></a>
# MAGIC ***
# MAGIC Feature scaling is an important concept of machine learning models. Often times a dataset contain features highly varying in magnitude and unit. For some machine learning models, it is not a problem. However, for many other ones, its quite a problem. Many machine learning algorithms uses euclidian distances to calculate the distance between two points, it is quite a problem. Let's again look at a the sample of the **train** dataset below.

# COMMAND ----------

train.sample(5)

# COMMAND ----------

# MAGIC %md
# MAGIC Here **Age** and **Calculated_fare** is much higher in magnitude compared to others machine learning features. This can create problems as many machine learning models will get confused thinking **Age** and **Calculated_fare** have higher weight than other features. Therefore, we need to do feature scaling to get a better result. 
# MAGIC There are multiple ways to do feature scaling. 
# MAGIC <ul>
# MAGIC     <li><b>MinMaxScaler</b>-Scales the data using the max and min values so that it fits between 0 and 1.</li>
# MAGIC     <li><b>StandardScaler</b>-Scales the data so that it has mean 0 and variance of 1.</li>
# MAGIC     <li><b>RobustScaler</b>-Scales the data similary to Standard Scaler, but makes use of the median and scales using the interquertile range so as to aviod issues with large outliers.</b>
# MAGIC  </ul>
# MAGIC I will discuss more on that in a different kernel. For now we will use <b>Standard Scaler</b> to feature scale our dataset. 
# MAGIC 
# MAGIC P.S. I am showing a sample of both before and after so that you can see how scaling changes the dataset.

# COMMAND ----------

# MAGIC %md
# MAGIC <h3><font color="$5831bc" face="Comic Sans MS">Before Scaling</font></h3>

# COMMAND ----------

headers = X_train.columns 

X_train.head()

# COMMAND ----------

# Feature Scaling
## We will be using standardscaler to transform
from sklearn.preprocessing import StandardScaler
st_scale = StandardScaler()

## transforming "train_x"
X_train = st_scale.fit_transform(X_train)
## transforming "test_x"
X_test = st_scale.transform(X_test)

## transforming "The testset"
#test = st_scale.transform(test)

# COMMAND ----------

# MAGIC %md
# MAGIC <h3><font color="#5831bc" face="Comic Sans MS">After Scaling</font></h3>

# COMMAND ----------

pd.DataFrame(X_train, columns=headers).head()

# COMMAND ----------

# MAGIC %md
# MAGIC You can see how the features have transformed above.

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 7: Modeling the Data
# MAGIC <a id="modelingthedata"></a>
# MAGIC ***
# MAGIC In the previous versions of this kernel, I thought about explaining each model before applying it. However, this process makes this kernel too lengthy to sit and read at one go. Therefore I have decided to break this kernel down and explain each algorithm in a different kernel and add the links here. If you like to review logistic regression, please click [here](https://www.kaggle.com/masumrumi/logistic-regression-with-titanic-dataset).

# COMMAND ----------

# import LogisticRegression model in python. 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, accuracy_score

## call on the model object
logreg = LogisticRegression(solver='liblinear',
                            penalty= 'l1',random_state = 42
                                
                            )

## fit the model with "train_x" and "train_y"
logreg.fit(X_train,y_train)

## Once the model is trained we want to find out how well the model is performing, so we test the model. 
## we use "X_test" portion of the data(this data was not used to fit the model) to predict model outcome. 
y_pred = logreg.predict(X_test)

## Once predicted we save that outcome in "y_pred" variable.
## Then we compare the predicted value( "y_pred") and actual value("test_y") to see how well our model is performing. 

# COMMAND ----------

# MAGIC %md
# MAGIC <h1><font color="#5831bc" face="Comic Sans MS">Evaluating a classification model</font></h1>
# MAGIC 
# MAGIC There are multiple ways to evaluate a classification model. 
# MAGIC 
# MAGIC * Confusion Matrix. 
# MAGIC * ROC Curve
# MAGIC * AUC Curve. 
# MAGIC 
# MAGIC 
# MAGIC ## Confusion Matrix
# MAGIC <b>Confusion matrix</b>, a table that <b>describes the performance of a classification model</b>. Confusion Matrix tells us how many our model predicted correctly and incorrectly in terms of binary/multiple outcome classes by comparing actual and predicted cases. For example, in terms of this dataset, our model is a binary one and we are trying to classify whether the passenger survived or not survived. we have fit the model using **X_train** and **y_train** and predicted the outcome of **X_test** in the variable **y_pred**. So, now we will use a confusion matrix to compare between **y_test** and **y_pred**. Let's do the confusion matrix.

# COMMAND ----------

from sklearn.metrics import classification_report, confusion_matrix
# printing confision matrix
pd.DataFrame(confusion_matrix(y_test,y_pred),\
            columns=["Predicted Not-Survived", "Predicted Survived"],\
            index=["Not-Survived","Survived"] )

# COMMAND ----------

# MAGIC %md
# MAGIC Our **y_test** has a total of 294 data points; part of the original train set that we splitted in order to evaluate our model. Each number here represents certain details about our model. If we were to think about this interms of column and raw, we could see that...
# MAGIC 
# MAGIC * the first column is of data points that the machine predicted as not-survived.
# MAGIC * the second column is of the statistics that the model predicted as survievd.
# MAGIC * In terms of raws, the first raw indexed as "Not-survived" means that the value in that raw are actual statistics of not survived once. 
# MAGIC * and the "Survived" indexed raw are values that actually survived.
# MAGIC 
# MAGIC Now you can see that the predicted not-survived and predicted survived sort of overlap with actual survived and actual not-survived. After all it is a matrix and we have some terminologies to call these statistics more specifically. Let's see what they are

# COMMAND ----------

# MAGIC %md
# MAGIC <ul style="list-style-type:square;">
# MAGIC     <li><b>True Positive(TP)</b>: values that the model predicted as yes(survived) and is actually yes(survived).</li>
# MAGIC     <li><b>True Negative(TN)</b>: values that model predicted as no(not-survived) and is actually no(not-survived)</li>
# MAGIC     <li><b>False Positive(or Type I error)</b>: values that model predicted as yes(survived) but actually no(not-survived)</li>
# MAGIC     <li><b>False Negative(or Type II error)</b>: values that model predicted as no(not-survived) but actually yes(survived)</li>
# MAGIC </ul>
# MAGIC 
# MAGIC For this dataset, whenever the model is predicting something as yes, it means the model is predicting that the passenger survived and for cases when the model predicting no; it means the passenger did not survive. Let's determine the value of all these terminologies above.
# MAGIC <ul style="list-style-type:square;">
# MAGIC     <li><b>True Positive(TP):87</b></li>
# MAGIC     <li><b>True Negative(TN):149</b></li>
# MAGIC     <li><b>False Positive(FP):28</b></li>
# MAGIC     <li><b>False Negative(FN):30</b></li>
# MAGIC </ul>
# MAGIC From these four terminologies, we can compute many other rates that are used to evaluate a binary classifier. 
# MAGIC 
# MAGIC 
# MAGIC #### Accuracy: 
# MAGIC ** Accuracy is the measure of how often the model is correct.** 
# MAGIC * (TP + TN)/total = (87+149)/294 = .8027
# MAGIC 
# MAGIC We can also calculate accuracy score using scikit learn.

# COMMAND ----------

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

# COMMAND ----------

# MAGIC %md
# MAGIC **Misclassification Rate:** Misclassification Rate is the measure of how often the model is wrong**
# MAGIC * Misclassification Rate and Accuracy are opposite of each other.
# MAGIC * Missclassification is equivalent to 1 minus Accuracy. 
# MAGIC * Misclassification Rate is also known as "Error Rate".
# MAGIC 
# MAGIC > (FP + FN)/Total = (28+30)/294 = 0.19
# MAGIC 
# MAGIC **True Positive Rate/Recall/Sensitivity:** How often the model predicts yes(survived) when it's actually yes(survived)?
# MAGIC > TP/(TP+FN) = 87/(87+30) = 0.7435897435897436

# COMMAND ----------

from sklearn.metrics import recall_score
recall_score(y_test, y_pred)

# COMMAND ----------

# MAGIC %md
# MAGIC **False Positive Rate:** How often the model predicts yes(survived) when it's actually no(not-survived)?
# MAGIC > FP/(FP+TN) = 28/(28+149) = 0.15819209039548024
# MAGIC 
# MAGIC **True Negative Rate/Specificity:** How often the model predicts no(not-survived) when it's actually no(not-survived)?
# MAGIC * True Negative Rate is equivalent to 1 minus False Positive Rate.
# MAGIC 
# MAGIC > TN/(TN+FP) = 149/(149+28) = 0.8418079096045198
# MAGIC 
# MAGIC **Precision:** How often is it correct when the model predicts yes. 
# MAGIC > TP/(TP+FP) = 87/(87+28) = 0.7565217391304347

# COMMAND ----------

from sklearn.metrics import precision_score
precision_score(y_test, y_pred)

# COMMAND ----------

from sklearn.metrics import classification_report, balanced_accuracy_score
print(classification_report(y_test, y_pred))

# COMMAND ----------

# MAGIC %md
# MAGIC we have our confusion matrix. How about we give it a little more character.

# COMMAND ----------

from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


np.set_printoptions(precision=2)

class_names = np.array(['not_survived','survived'])

# Plot non-normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=class_names,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC <h1>AUC & ROC Curve</h1>

# COMMAND ----------

from sklearn.metrics import roc_curve, auc
#plt.style.use('seaborn-pastel')
y_score = logreg.decision_function(X_test)

FPR, TPR, _ = roc_curve(y_test, y_score)
ROC_AUC = auc(FPR, TPR)
print (ROC_AUC)

plt.figure(figsize =[11,9])
plt.plot(FPR, TPR, label= 'ROC curve(area = %0.2f)'%ROC_AUC, linewidth= 4)
plt.plot([0,1],[0,1], 'k--', linewidth = 4)
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.05])
plt.xlabel('False Positive Rate', fontsize = 18)
plt.ylabel('True Positive Rate', fontsize = 18)
plt.title('ROC for Titanic survivors', fontsize= 18)
plt.show()

# COMMAND ----------

from sklearn.metrics import precision_recall_curve

y_score = logreg.decision_function(X_test)

precision, recall, _ = precision_recall_curve(y_test, y_score)
PR_AUC = auc(recall, precision)

plt.figure(figsize=[11,9])
plt.plot(recall, precision, label='PR curve (area = %0.2f)' % PR_AUC, linewidth=4)
plt.xlabel('Recall', fontsize=18)
plt.ylabel('Precision', fontsize=18)
plt.title('Precision Recall Curve for Titanic survivors', fontsize=18)
plt.legend(loc="lower right")
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Using Cross-validation:
# MAGIC Pros: 
# MAGIC * Helps reduce variance. 
# MAGIC * Expends models predictability.

# COMMAND ----------

sc = st_scale

# COMMAND ----------

## Using StratifiedShuffleSplit
## We can use KFold, StratifiedShuffleSplit, StratiriedKFold or ShuffleSplit, They are all close cousins. look at sklearn userguide for more info.   
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
cv = StratifiedShuffleSplit(n_splits = 10, test_size = .25, random_state = 0 ) # run model 10x with 60/30 split intentionally leaving out 10%
## Using standard scale for the whole dataset.

## saving the feature names for decision tree display
column_names = X.columns

X = sc.fit_transform(X)
accuracies = cross_val_score(LogisticRegression(solver='liblinear'), X,y, cv  = cv)
print ("Cross-Validation accuracy scores:{}".format(accuracies))
print ("Mean Cross-Validation accuracy score: {}".format(round(accuracies.mean(),5)))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Grid Search on Logistic Regression
# MAGIC * What is grid search? 
# MAGIC * What are the pros and cons?
# MAGIC 
# MAGIC **Gridsearch** is a simple concept but effective technique in Machine Learning. The word **GridSearch** stands for the fact that we are searching for optimal parameter/parameters over a "grid." These optimal parameters are also known as **Hyperparameters**. **The Hyperparameters are model parameters that are set before fitting the model and determine the behavior of the model.**. For example, when we choose to use linear regression, we may decide to add a penalty to the loss function such as Ridge or Lasso. These penalties require specific alpha (the strength of the regularization technique) to set beforehand. The higher the value of alpha, the more penalty is being added. GridSearch finds the optimal value of alpha among a range of values provided by us, and then we go on and use that optimal value to fit the model and get sweet results. It is essential to understand those model parameters are different from models outcomes, for example, **coefficients** or model evaluation metrics such as **accuracy score** or **mean squared error** are model outcomes and different than hyperparameters.
# MAGIC 
# MAGIC #### This part of the kernel is a working progress. Please check back again for future updates.####

# COMMAND ----------

from sklearn.model_selection import GridSearchCV, StratifiedKFold
## C_vals is the alpla value of lasso and ridge regression(as alpha increases the model complexity decreases,)
## remember effective alpha scores are 0<alpha<infinity 
C_vals = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,16.5,17,17.5,18]
## Choosing penalties(Lasso(l1) or Ridge(l2))
penalties = ['l1','l2']
## Choose a cross validation strategy. 
cv = StratifiedShuffleSplit(n_splits = 10, test_size = .25)

## setting param for param_grid in GridSearchCV. 
param = {'penalty': penalties, 'C': C_vals}

logreg = LogisticRegression(solver='liblinear')
## Calling on GridSearchCV object. 
grid = GridSearchCV(estimator=LogisticRegression(), 
                           param_grid = param,
                           scoring = 'accuracy',
                            n_jobs =-1,
                           cv = cv
                          )
## Fitting the model
grid.fit(X, y)

# COMMAND ----------

## Getting the best of everything. 
print (grid.best_score_)
print (grid.best_params_)
print(grid.best_estimator_)



# COMMAND ----------

# MAGIC %md
# MAGIC #### Using the best parameters from the grid-search.

# COMMAND ----------

### Using the best parameters from the grid-search.
logreg_grid = grid.best_estimator_
logreg_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC #### This part of the kernel is a working progress. Please check back again for future updates.####
# MAGIC  
# MAGIC  Resources: 
# MAGIC  * [Confusion Matrix](https://www.youtube.com/watch?v=8Oog7TXHvFY)
# MAGIC ### Under-fitting & Over-fitting: 
# MAGIC So, we have our first model and its score. But, how do we make sure that our model is performing well. Our model may be overfitting or underfitting. In fact, for those of you don't know what overfitting and underfitting is, Let's find out.
# MAGIC 
# MAGIC ![](https://cdncontribute.geeksforgeeks.org/wp-content/uploads/fittings.jpg)
# MAGIC 
# MAGIC As you see in the chart above. **Underfitting** is when the model fails to capture important aspects of the data and therefore introduces more bias and performs poorly. On the other hand, **Overfitting** is when the model performs too well on the training data but does poorly in the validation set or test sets.  This situation is also known as having less bias but more variation and perform poorly as well. Ideally, we want to configure a model that performs well not only in the training data but also in the test data. This is where **bias-variance tradeoff** comes in. When we have a model that overfits, meaning less biased and more of variance, we introduce some bias in exchange of having much less variance. One particular tactic for this task is regularization models (Ridge, Lasso, Elastic Net).  These models are built to deal with the bias-variance tradeoff. This [kernel](https://www.kaggle.com/dansbecker/underfitting-and-overfitting) explains this topic well. Also, the following chart gives us a mental picture of where we want our models to be. 
# MAGIC ![](http://scott.fortmann-roe.com/docs/docs/BiasVariance/biasvariance.png)
# MAGIC 
# MAGIC Ideally, we want to pick a sweet spot where the model performs well in training set, validation set, and test set. As the model gets complex, bias decreases, variance increases. However, the most critical part is the error rates. We want our models to be at the bottom of that **U** shape where the error rate is the least. That sweet spot is also known as **Optimum Model Complexity(OMC).**
# MAGIC 
# MAGIC Now that we know what we want in terms of under-fitting and over-fitting, let's talk about how to combat them. 
# MAGIC 
# MAGIC How to combat over-fitting?
# MAGIC <ul>
# MAGIC     <li>Simplify the model by using less parameters.</li>
# MAGIC     <li>Simplify the model by changing the hyperparameters.</li>
# MAGIC     <li>Introducing regularization models. </li>
# MAGIC     <li>Use more training data. </li>
# MAGIC     <li>Gatter more data ( and gather better quality data). </li>
# MAGIC     </ul>
# MAGIC  #### This part of the kernel is a working progress. Please check back again for future updates.####

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7b. K-Nearest Neighbor classifier(KNN)
# MAGIC <a id="knn"></a>
# MAGIC ***

# COMMAND ----------

## Importing the model. 
from sklearn.neighbors import KNeighborsClassifier
## calling on the model oject. 
knn = KNeighborsClassifier(metric='minkowski', p=2)
## knn classifier works by doing euclidian distance 


## doing 10 fold staratified-shuffle-split cross validation 
cv = StratifiedShuffleSplit(n_splits=10, test_size=.25, random_state=2)

accuracies = cross_val_score(knn, X,y, cv = cv, scoring='accuracy')
print ("Cross-Validation accuracy scores:{}".format(accuracies))
print ("Mean Cross-Validation accuracy score: {}".format(round(accuracies.mean(),3)))

# COMMAND ----------

# MAGIC %md
# MAGIC #### Manually find the best possible k value for KNN

# COMMAND ----------

## Search for an optimal value of k for KNN.
k_range = range(1,31)
k_scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X,y, cv = cv, scoring = 'accuracy')
    k_scores.append(scores.mean())
print("Accuracy scores are: {}\n".format(k_scores))
print ("Mean accuracy score: {}".format(np.mean(k_scores)))


# COMMAND ----------

from matplotlib import pyplot as plt
plt.plot(k_range, k_scores)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Grid search on KNN classifier

# COMMAND ----------

from sklearn.model_selection import GridSearchCV
## trying out multiple values for k
k_range = range(1,31)
## 
weights_options=['uniform','distance']
# 
param = {'n_neighbors':k_range, 'weights':weights_options}
## Using startifiedShufflesplit. 
cv = StratifiedShuffleSplit(n_splits=10, test_size=.30, random_state=15)
# estimator = knn, param_grid = param, n_jobs = -1 to instruct scikit learn to use all available processors. 
grid = GridSearchCV(KNeighborsClassifier(), param,cv=cv,verbose = False, n_jobs=-1)
## Fitting the model. 
grid.fit(X,y)

# COMMAND ----------

print(grid.best_score_)
print(grid.best_params_)
print(grid.best_estimator_)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Using best estimator from grid search using KNN.

# COMMAND ----------

### Using the best parameters from the grid-search.
knn_grid= grid.best_estimator_
knn_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Using RandomizedSearchCV
# MAGIC Randomized search is a close cousin of grid search. It doesn't  always provide the best result but its fast.

# COMMAND ----------

from sklearn.model_selection import RandomizedSearchCV
## trying out multiple values for k
k_range = range(1,31)
## 
weights_options=['uniform','distance']
# 
param = {'n_neighbors':k_range, 'weights':weights_options}
## Using startifiedShufflesplit. 
cv = StratifiedShuffleSplit(n_splits=10, test_size=.30)
# estimator = knn, param_grid = param, n_jobs = -1 to instruct scikit learn to use all available processors. 
## for RandomizedSearchCV, 
grid = RandomizedSearchCV(KNeighborsClassifier(), param,cv=cv,verbose = False, n_jobs=-1, n_iter=40)
## Fitting the model. 
grid.fit(X,y)

# COMMAND ----------

print (grid.best_score_)
print (grid.best_params_)
print(grid.best_estimator_)

# COMMAND ----------

### Using the best parameters from the grid-search.
knn_ran_grid = grid.best_estimator_
knn_ran_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gaussian Naive Bayes
# MAGIC <a id="gaussian_naive"></a>
# MAGIC ***

# COMMAND ----------

# Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

gaussian = GaussianNB()
gaussian.fit(X, y)
y_pred = gaussian.predict(X_test)
gaussian_accy = round(accuracy_score(y_pred, y_test), 3)
print(gaussian_accy)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Support Vector Machines(SVM)
# MAGIC <a id="svm"></a>
# MAGIC ***

# COMMAND ----------

from sklearn.svm import SVC
Cs = [0.001, 0.01, 0.1, 1,1.5,2,2.5,3,4,5, 10] ## penalty parameter C for the error term. 
gammas = [0.0001,0.001, 0.01, 0.1, 1]
param_grid = {'C': Cs, 'gamma' : gammas}
cv = StratifiedShuffleSplit(n_splits=10, test_size=.30, random_state=15)
grid_search = GridSearchCV(SVC(kernel = 'rbf', probability=True), param_grid, cv=cv) ## 'rbf' stands for gaussian kernel
grid_search.fit(X,y)

# COMMAND ----------

print(grid_search.best_score_)
print(grid_search.best_params_)
print(grid_search.best_estimator_)

# COMMAND ----------

# using the best found hyper paremeters to get the score. 
svm_grid = grid_search.best_estimator_
svm_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Decision Tree Classifier
# MAGIC 
# MAGIC Decision tree works by breaking down the dataset into small subsets. This breaking down process is done by asking questions about the features of the datasets. The idea is to unmix the labels by asking fewer questions necessary. As we ask questions, we are breaking down the dataset into more subsets. Once we have a subgroup with only the unique type of labels, we end the tree in that node. If you would like to get a detailed understanding of Decision tree classifier, please take a look at [this](https://www.kaggle.com/masumrumi/decision-tree-with-titanic-dataset) kernel.

# COMMAND ----------

from sklearn.tree import DecisionTreeClassifier
max_depth = range(1,30)
max_feature = [21,22,23,24,25,26,28,29,30,'auto']
criterion=["entropy", "gini"]

param = {'max_depth':max_depth, 
         'max_features':max_feature, 
         'criterion': criterion}
grid = GridSearchCV(DecisionTreeClassifier(), 
                                param_grid = param, 
                                 verbose=False, 
                                 cv=StratifiedKFold(n_splits=20, random_state=15, shuffle=True),
                                n_jobs = -1)
grid.fit(X, y) 

# COMMAND ----------

print( grid.best_params_)
print (grid.best_score_)
print (grid.best_estimator_)

# COMMAND ----------

dectree_grid = grid.best_estimator_
## using the best found hyper paremeters to get the score. 
dectree_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC <h4> Let's look at the feature importance from decision tree grid.</h4>

# COMMAND ----------

## feature importance
feature_importances = pd.DataFrame(dectree_grid.feature_importances_,
                                   index = column_names,
                                    columns=['importance'])
feature_importances.sort_values(by='importance', ascending=False).head(10)

# COMMAND ----------

# MAGIC %md
# MAGIC These are the top 10 features determined by **Decision Tree** helped classifing the fates of many passenger on Titanic on that night.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7f. Random Forest Classifier
# MAGIC <a id="random_forest"></a>

# COMMAND ----------

# MAGIC %md
# MAGIC I admire working with decision trees because of the potential and basics they provide towards building a more complex model like Random Forest(RF). RF is an ensemble method (combination of many decision trees) which is where the "forest" part comes in. One crucial details about Random Forest is that while using a forest of decision trees, RF model <b>takes random subsets of the original dataset(bootstrapped)</b> and <b>random subsets of the variables(features/columns)</b>. Using this method, the RF model creates 100's-1000's(the amount can be menually determined) of a wide variety of decision trees. This variety makes the RF model more effective and accurate. We then run each test data point through all of these 100's to 1000's of decision trees or the RF model and take a vote on the output.

# COMMAND ----------

from sklearn.model_selection import GridSearchCV, StratifiedKFold, StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
n_estimators = [140,145,150,155,160];
max_depth = range(1,10);
criterions = ['gini', 'entropy'];
cv = StratifiedShuffleSplit(n_splits=10, test_size=.30, random_state=15)


parameters = {'n_estimators':n_estimators,
              'max_depth':max_depth,
              'criterion': criterions
              
        }
grid = GridSearchCV(estimator=RandomForestClassifier(max_features='auto'),
                                 param_grid=parameters,
                                 cv=cv,
                                 n_jobs = -1)
grid.fit(X,y) 

# COMMAND ----------

print (grid.best_score_)
print (grid.best_params_)
print (grid.best_estimator_)

# COMMAND ----------

rf_grid = grid.best_estimator_
rf_grid.score(X,y)

# COMMAND ----------

from sklearn.metrics import classification_report
# Print classification report for y_test
print(classification_report(y_test, y_pred, labels=rf_grid.classes_))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Feature Importance

# COMMAND ----------

## feature importance
feature_importances = pd.DataFrame(rf_grid.feature_importances_,
                                   index = column_names,
                                    columns=['importance'])
feature_importances.sort_values(by='importance', ascending=False).head(10)

# COMMAND ----------

# MAGIC %md
# MAGIC <h3>Why Random Forest?(Pros and Cons)</h3>

# COMMAND ----------

# MAGIC %md
# MAGIC ***
# MAGIC <h2>Introducing Ensemble Learning</h2>
# MAGIC In statistics and machine learning, ensemble methods use multiple learning algorithms to obtain better predictive performance than could be obtained from any of the constituent learning algorithms alone. 
# MAGIC 
# MAGIC There are two types of ensemple learnings. 
# MAGIC 
# MAGIC **Bagging/Averaging Methods**
# MAGIC > In averaging methods, the driving principle is to build several estimators independently and then to average their predictions. On average, the combined estimator is usually better than any of the single base estimator because its variance is reduced.
# MAGIC 
# MAGIC **Boosting Methods**
# MAGIC > The other family of ensemble methods are boosting methods, where base estimators are built sequentially and one tries to reduce the bias of the combined estimator. The motivation is to combine several weak models to produce a powerful ensemble.
# MAGIC 
# MAGIC <h4 align="right">Source:GA</h4>
# MAGIC 
# MAGIC Resource: <a href="https://towardsdatascience.com/ensemble-methods-bagging-boosting-and-stacking-c9214a10a205">Ensemble methods: bagging, boosting and stacking</a>
# MAGIC ***
# MAGIC ## 7g. Bagging Classifier
# MAGIC <a id="bagging"></a>
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html">Bagging Classifier</a>(Bootstrap Aggregating) is the ensemble method that involves manipulating the training set by resampling and running algorithms on it. Let's do a quick review:
# MAGIC * Bagging classifier uses a process called bootstrapped dataset to create multiple datasets from one original dataset and runs algorithm on each one of them. Here is an image to show how bootstrapped dataset works. 
# MAGIC <img src="https://uc-r.github.io/public/images/analytics/bootstrap/bootstrap.png" width="600">
# MAGIC <h4 align="center">Resampling from original dataset to bootstrapped datasets</h4>
# MAGIC <h4 align="right">Source: https://uc-r.github.io</h4>
# MAGIC 
# MAGIC 
# MAGIC * After running a learning algorithm on each one of the bootstrapped datasets, all models are combined by taking their average. the test data/new data then go through this averaged classifier/combined classifier and predict the output. 
# MAGIC 
# MAGIC Here is an image to make it clear on how bagging works, 
# MAGIC <img src="https://prachimjoshi.files.wordpress.com/2015/07/screen_shot_2010-12-03_at_5-46-21_pm.png" width="600">
# MAGIC <h4 align="right">Source: https://prachimjoshi.files.wordpress.com</h4>
# MAGIC Please check out [this](https://www.kaggle.com/masumrumi/bagging-with-titanic-dataset) kernel if you want to find out more about bagging classifier.

# COMMAND ----------

from sklearn.ensemble import BaggingClassifier
n_estimators = [10,30,50,70,80,150,160, 170,175,180,185];
cv = StratifiedShuffleSplit(n_splits=10, test_size=.30, random_state=15)

parameters = {'n_estimators':n_estimators,
              
        }
grid = GridSearchCV(BaggingClassifier(base_estimator= None, ## If None, then the base estimator is a decision tree.
                                      bootstrap_features=False),
                                 param_grid=parameters,
                                 cv=cv,
                                 n_jobs = -1)
grid.fit(X,y) 

# COMMAND ----------

print (grid.best_score_)
print (grid.best_params_)
print (grid.best_estimator_)

# COMMAND ----------

bagging_grid = grid.best_estimator_
bagging_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC <h3>Why use Bagging? (Pros and cons)</h3>
# MAGIC Bagging works best with strong and complex models(for example, fully developed decision trees). However, don't let that fool you to thinking that similar to a decision tree, bagging also overfits the model. Instead, bagging reduces overfitting since a lot of the sample training data are repeated and used to create base estimators. With a lot of equally likely training data, bagging is not very susceptible to overfitting with noisy data, therefore reduces variance. However, the downside is that this leads to an increase in bias.

# COMMAND ----------

# MAGIC %md
# MAGIC <h4>Random Forest VS. Bagging Classifier</h4>
# MAGIC 
# MAGIC If some of you are like me, you may find Random Forest to be similar to Bagging Classifier. However, there is a fundamental difference between these two which is **Random Forests ability to pick subsets of features in each node.** I will elaborate on this in a future update.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7h. AdaBoost Classifier
# MAGIC <a id="AdaBoost"></a>
# MAGIC ***
# MAGIC AdaBoost is another <b>ensemble model</b> and is quite different than Bagging. Let's point out the core concepts. 
# MAGIC > AdaBoost combines a lot of "weak learners"(they are also called stump; a tree with only one node and two leaves) to make classifications.
# MAGIC 
# MAGIC > This base model fitting is an iterative process where each stump is chained one after the other; <b>It cannot run in parallel.</b>
# MAGIC 
# MAGIC > <b>Some stumps get more say in the final classifications than others.</b> The models use weights that are assigned to each data point/raw indicating their "importance." Samples with higher weight have a higher influence on the total error of the next model and gets more priority. The first stump starts with uniformly distributed weight which means, in the beginning, every datapoint have an equal amount of weights. 
# MAGIC 
# MAGIC > <b>Each stump is made by talking the previous stump's mistakes into account.</b> After each iteration weights gets re-calculated in order to take the errors/misclassifications from the last stump into consideration. 
# MAGIC 
# MAGIC > The final prediction is typically constructed by a weighted vote where weights for each base model depends on their training errors or misclassification rates. 
# MAGIC 
# MAGIC To illustrate what we have talked about so far let's look at the following visualization. 
# MAGIC 
# MAGIC <img src="https://cdn-images-1.medium.com/max/1600/0*paPv7vXuq4eBHZY7.png">
# MAGIC <h5 align="right"> Source: Diogo(Medium)</h5>
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC Let's dive into each one of the nitty-gritty stuff about AdaBoost:
# MAGIC ***
# MAGIC > <b>First</b>, we determine the best feature to split the dataset using Gini index(basics from decision tree). The feature with the lowest Gini index becomes the first stump in the AdaBoost stump chain(the lower the Gini index is, the better unmixed the label is, therefore, better split).
# MAGIC ***
# MAGIC > <b>Secondly</b>, we need to determine how much say a stump will have in the final classification and how we can calculate that.
# MAGIC * We learn how much say a stump has in the final classification by calculating how well it classified the samples (aka calculate the total error of the weight).
# MAGIC * The <b>Total Error</b> for a stump is the sum of the weights associated with the incorrectly classified samples. For example, lets say, we start a stump with 10 datasets. The first stump will uniformly distribute an weight amoung all the datapoints. Which means each data point will have 1/10 weight. Let's say once the weight is distributed we run the model and find 2 incorrect predicitons. In order to calculate the total erorr we add up all the misclassified weights. Here we get 1/10 + 1/10 = 2/10 or 1/5. This is our total error. We can also think about it
# MAGIC 
# MAGIC 
# MAGIC $$ \epsilon_t = \frac{\text{misclassifications}_t}{\text{observations}_t} $$
# MAGIC 
# MAGIC 
# MAGIC * Since the weight is uniformly distributed(all add up to 1) among all data points, the total error will always be between 0(perfect stump) and 1(horrible stump).
# MAGIC * We use the total error to determine the amount of say a stump has in the final classification using the following formula
# MAGIC  
# MAGIC 
# MAGIC $$ \alpha_t = \frac{1}{2}ln \left(\frac{1-\epsilon_t}{\epsilon_t}\right) \text{where } \epsilon_t < 1$$
# MAGIC 
# MAGIC 
# MAGIC Where $\epsilon_t$ is the misclassification rate for the current classifier:
# MAGIC 
# MAGIC 
# MAGIC $$ \epsilon_t = \frac{\text{misclassifications}_t}{\text{observations}_t} $$
# MAGIC 
# MAGIC 
# MAGIC Here...
# MAGIC * $\alpha_t$ = Amount of Say
# MAGIC * $\epsilon_t$ = Total error
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC We can draw a graph to determine the amount of say using the value of total error(0 to 1)
# MAGIC 
# MAGIC <img src="http://chrisjmccormick.files.wordpress.com/2013/12/adaboost_alphacurve.png">
# MAGIC <h5 align="right"> Source: Chris McCormick</h5>
# MAGIC 
# MAGIC * The blue line tells us the amount of say for <b>Total Error(Error rate)</b> between 0 and 1. 
# MAGIC * When the stump does a reasonably good job, and the <b>total error</b> is minimal, then the <b>amount of say(Alpha)</b> is relatively large, and the alpha value is positive. 
# MAGIC * When the stump does an average job(similar to a coin flip/the ratio of getting correct and incorrect ~50%/50%), then the <b>total error</b> is ~0.5. In this case the <b>amount of say</b> is <b>0</b>.
# MAGIC * When the error rate is high let's say close to 1, then the <b>amount of say</b> will be negative, which means if the stump outputs a value as "survived" the included weight will turn that value into "not survived."
# MAGIC 
# MAGIC P.S. If the <b>Total Error</b> is 1 or 0, then this equation will freak out. A small amount of error is added to prevent this from happening. 
# MAGIC  
# MAGIC  ***
# MAGIC > <b>Third</b>, We need to learn how to modify the weights so that the next stump will take the errors that the current stump made into account. The pseducode for calculating the new sample weight is as follows. 
# MAGIC 
# MAGIC 
# MAGIC $$ New Sample Weight = Sample Weight + e^{\alpha_t}$$
# MAGIC 
# MAGIC Here the $\alpha_t(AmountOfSay)$ can be positive or negative depending whether the sample was correctly classified or misclassified by the current stump. We want to increase the sample weight of the misclassified samples; hinting the next stump to put more emphasize on those. Inversely, we want to decrease the sample weight of the correctly classified samples; hinting the next stump to put less emphasize on those. 
# MAGIC 
# MAGIC The following equation help us to do this calculation. 
# MAGIC 
# MAGIC $$ D_{t+1}(i) = D_t(i) e^{-\alpha_t y_i h_t(x_i)} $$
# MAGIC 
# MAGIC Here, 
# MAGIC * $D_{t+1}(i)$ = New Sample Weight. 
# MAGIC * $D_t(i)$ = Current Sample weight.
# MAGIC * $\alpha_t$ = Amount of Say, alpha value, this is the coefficient that gets updated in each iteration and 
# MAGIC * $y_i h_t(x_i)$ = place holder for 1 if stump correctly classified, -1 if misclassified. 
# MAGIC 
# MAGIC Finally, we put together the combined classifier, which is 
# MAGIC 
# MAGIC $$ AdaBoost(X) = sign\left(\sum_{t=1}^T\alpha_t h_t(X)\right) $$ 
# MAGIC 
# MAGIC Here, 
# MAGIC 
# MAGIC $AdaBoost(X)$ is the classification predictions for $y$ using predictor matrix $X$
# MAGIC 
# MAGIC $T$ is the set of "weak learners"
# MAGIC 
# MAGIC $\alpha_t$ is the contribution weight for weak learner $t$
# MAGIC 
# MAGIC $h_t(X)$ is the prediction of weak learner $t$
# MAGIC 
# MAGIC and $y$ is binary **with values -1 and 1**
# MAGIC 
# MAGIC 
# MAGIC P.S. Since the stump barely captures essential specs about the dataset, the model is highly biased in the beginning. However, as the chain of stumps continues and at the end of the process, AdaBoost becomes a strong tree and reduces both bias and variance.
# MAGIC 
# MAGIC <h3>Resources:</h3>
# MAGIC <ul>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=LsK-xG1cLYA">Statquest</a></li>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=-DUxtdeCiB4">Principles of Machine Learning | AdaBoost(Video)</a></li>
# MAGIC </ul>

# COMMAND ----------

from sklearn.ensemble import AdaBoostClassifier
n_estimators = [100,140,145,150,160, 170,175,180,185];
cv = StratifiedShuffleSplit(n_splits=10, test_size=.30, random_state=15)
learning_r = [0.1,1,0.01,0.5]

parameters = {'n_estimators':n_estimators,
              'learning_rate':learning_r
              
        }
grid = GridSearchCV(AdaBoostClassifier(base_estimator= None, ## If None, then the base estimator is a decision tree.
                                     ),
                                 param_grid=parameters,
                                 cv=cv,
                                 n_jobs = -1)
grid.fit(X,y) 

# COMMAND ----------

print (grid.best_score_)
print (grid.best_params_)
print (grid.best_estimator_)

# COMMAND ----------

adaBoost_grid = grid.best_estimator_
adaBoost_grid.score(X,y)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pros and cons of boosting
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ### Pros
# MAGIC 
# MAGIC - Achieves higher performance than bagging when hyper-parameters tuned properly.
# MAGIC - Can be used for classification and regression equally well.
# MAGIC - Easily handles mixed data types.
# MAGIC - Can use "robust" loss functions that make the model resistant to outliers.
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ### Cons
# MAGIC 
# MAGIC - Difficult and time consuming to properly tune hyper-parameters.
# MAGIC - Cannot be parallelized like bagging (bad scalability when huge amounts of data).
# MAGIC - More risk of overfitting compared to bagging.
# MAGIC 
# MAGIC <h3>Resources: </h3>
# MAGIC <ul>
# MAGIC     <li><a href="http://mccormickml.com/2013/12/13/adaboost-tutorial/">AdaBoost Tutorial-Chris McCormick</a></li>
# MAGIC     <li><a href="http://rob.schapire.net/papers/explaining-adaboost.pdf">Explaining AdaBoost by Robert Schapire(One of the original author of AdaBoost)</a></li>
# MAGIC </ul>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7i. Gradient Boosting Classifier
# MAGIC <a id="gradient_boosting"></a>
# MAGIC ***

# COMMAND ----------

# Gradient Boosting Classifier
from sklearn.ensemble import GradientBoostingClassifier

gradient_boost = GradientBoostingClassifier()
gradient_boost.fit(X, y)
y_pred = gradient_boost.predict(X_test)
gradient_accy = round(accuracy_score(y_pred, y_test), 3)
print(gradient_accy)

# COMMAND ----------

# MAGIC %md
# MAGIC <div class=" alert alert-info">
# MAGIC <h3>Resources: </h3>
# MAGIC <ul>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=sDv4f4s2SB8">Gradient Descent(StatQuest)</a></li>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=3CC4N4z3GJc">Gradient Boost(Regression Main Ideas)(StatQuest)</a></li>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=3CC4N4z3GJc">Gradient Boost(Regression Calculation)(StatQuest)</a></li>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=jxuNLH5dXCs">Gradient Boost(Classification Main Ideas)(StatQuest)</a></li>
# MAGIC     <li><a href="https://www.youtube.com/watch?v=StWY5QWMXCw">Gradient Boost(Classification Calculation)(StatQuest)</a></li>
# MAGIC     <li><a href="https://www.analyticsvidhya.com/blog/2016/02/complete-guide-parameter-tuning-gradient-boosting-gbm-python/">Complete Machine Learning Guide to Parameter Tuning in Gradient Boosting (GBM) in Python</a></li>
# MAGIC </ul>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7j. XGBClassifier
# MAGIC <a id="XGBClassifier"></a>
# MAGIC ***

# COMMAND ----------

# from xgboost import XGBClassifier
# XGBClassifier = XGBClassifier()
# XGBClassifier.fit(X, y)
# y_pred = XGBClassifier.predict(X_test)
# XGBClassifier_accy = round(accuracy_score(y_pred, y_test), 3)
# print(XGBClassifier_accy)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7k. Extra Trees Classifier
# MAGIC <a id="extra_tree"></a>
# MAGIC ***

# COMMAND ----------

from sklearn.ensemble import ExtraTreesClassifier
ExtraTreesClassifier = ExtraTreesClassifier()
ExtraTreesClassifier.fit(X, y)
y_pred = ExtraTreesClassifier.predict(X_test)
extraTree_accy = round(accuracy_score(y_pred, y_test), 3)
print(extraTree_accy)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 7l. Gaussian Process Classifier
# MAGIC <a id="GaussianProcessClassifier"></a>
# MAGIC ***

# COMMAND ----------

from sklearn.gaussian_process import GaussianProcessClassifier
GaussianProcessClassifier = GaussianProcessClassifier()
GaussianProcessClassifier.fit(X, y)
y_pred = GaussianProcessClassifier.predict(X_test)
gau_pro_accy = round(accuracy_score(y_pred, y_test), 3)
print(gau_pro_accy)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7m. Voting Classifier
# MAGIC <a id="voting_classifer"></a>
# MAGIC ***

# COMMAND ----------

from sklearn.ensemble import VotingClassifier

voting_classifier = VotingClassifier(estimators=[
    ('lr_grid', logreg_grid),
    ('svc', svm_grid),
    ('random_forest', rf_grid),
    ('gradient_boosting', gradient_boost),
    ('decision_tree_grid',dectree_grid),
    ('knn_classifier', knn_grid),
#     ('XGB_Classifier', XGBClassifier),
    ('bagging_classifier', bagging_grid),
    ('adaBoost_classifier',adaBoost_grid),
    ('ExtraTrees_Classifier', ExtraTreesClassifier),
    ('gaussian_classifier',gaussian),
    ('gaussian_process_classifier', GaussianProcessClassifier)
],voting='hard')

#voting_classifier = voting_classifier.fit(train_x,train_y)
voting_classifier = voting_classifier.fit(X,y)

# COMMAND ----------

y_pred = voting_classifier.predict(X_test)
voting_accy = round(accuracy_score(y_pred, y_test), 3)
print(voting_accy)

# COMMAND ----------

#models = pd.DataFrame({
#    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
#              'Random Forest', 'Naive Bayes', 
#              'Decision Tree', 'Gradient Boosting Classifier', 'Voting Classifier', 'XGB Classifier','ExtraTrees Classifier','Bagging Classifier'],
#    'Score': [svc_accy, knn_accy, logreg_accy, 
#              random_accy, gaussian_accy, dectree_accy,
#               gradient_accy, voting_accy, XGBClassifier_accy, extraTree_accy, bagging_accy]})
#models.sort_values(by='Score', ascending=False)

# COMMAND ----------

# MAGIC %md
# MAGIC # Part 8: Submit test predictions
# MAGIC <a id="submit_predictions"></a>
# MAGIC ***

# COMMAND ----------

all_models = [logreg_grid,
              knn_grid, 
              knn_ran_grid,
              svm_grid,
              dectree_grid,
              rf_grid,
              bagging_grid,
              adaBoost_grid,
              voting_classifier]

c = {}
for i in all_models:
    a = i.predict(X_test)
    b = accuracy_score(a, y_test)
    c[i] = b
    


# COMMAND ----------

test_prediction = (max(c, key=c.get)).predict(test)
submission = pd.DataFrame({
        "PassengerId": passengerid,
        "Survived": test_prediction
    })

submission.PassengerId = submission.PassengerId.astype(int)
submission.Survived = submission.Survived.astype(int)

submission.to_csv("titanic1_submission.csv", index=False)

# COMMAND ----------

# MAGIC %md
# MAGIC <div class="alert alert-info">
# MAGIC     <h1>Resources</h1>
# MAGIC     <ul>
# MAGIC         <li><b>Statistics</b></li>
# MAGIC         <ul>
# MAGIC             <li><a href="https://statistics.laerd.com/statistical-guides/measures-of-spread-standard-deviation.php">Types of Standard Deviation</a></li>
# MAGIC             <li><a href="https://blog.minitab.com/blog/statistics-and-quality-data-analysis/what-is-a-t-test-and-why-is-it-like-telling-a-kid-to-clean-up-that-mess-in-the-kitchen">What Is a t-test? And Why Is It Like Telling a Kid to Clean Up that Mess in the Kitchen?</a></li>
# MAGIC             <li><a href="https://blog.minitab.com/blog/statistics-and-quality-data-analysis/what-are-t-values-and-p-values-in-statistics">What Are T Values and P Values in Statistics?</a></li>
# MAGIC             <li><a href="https://www.youtube.com/watch?v=E4KCfcVwzyw">What is p-value? How we decide on our confidence level.</a></li>
# MAGIC         </ul>
# MAGIC         <li><b>Writing pythonic code</b></li>
# MAGIC         <ul>
# MAGIC             <li><a href="https://www.kaggle.com/rtatman/six-steps-to-more-professional-data-science-code">Six steps to more professional data science code</a></li>
# MAGIC             <li><a href="https://www.kaggle.com/jpmiller/creating-a-good-analytics-report">Creating a Good Analytics Report</a></li>
# MAGIC             <li><a href="https://en.wikipedia.org/wiki/Code_smell">Code Smell</a></li>
# MAGIC             <li><a href="https://www.python.org/dev/peps/pep-0008/">Python style guides</a></li>
# MAGIC             <li><a href="https://gist.github.com/sloria/7001839">The Best of the Best Practices(BOBP) Guide for Python</a></li>
# MAGIC             <li><a href="https://www.python.org/dev/peps/pep-0020/">PEP 20 -- The Zen of Python</a></li>
# MAGIC             <li><a href="https://docs.python-guide.org/">The Hitchiker's Guide to Python</a></li>
# MAGIC             <li><a href="https://realpython.com/tutorials/best-practices/">Python Best Practice Patterns</a></li>
# MAGIC             <li><a href="http://www.nilunder.com/blog/2013/08/03/pythonic-sensibilities/">Pythonic Sensibilities</a></li>
# MAGIC         </ul>
# MAGIC         <li><b>Why Scikit-Learn?</b></li>
# MAGIC         <ul>
# MAGIC             <li><a href="https://www.oreilly.com/content/intro-to-scikit-learn/">Introduction to Scikit-Learn</a></li>
# MAGIC             <li><a href="https://www.oreilly.com/content/six-reasons-why-i-recommend-scikit-learn/">Six reasons why I recommend scikit-learn</a></li>
# MAGIC             <li><a href="https://hub.packtpub.com/learn-scikit-learn/">Why you should learn Scikit-learn</a></li>
# MAGIC             <li><a href="https://www.kaggle.com/baghern/a-deep-dive-into-sklearn-pipelines">A Deep Dive Into Sklearn Pipelines</a></li>
# MAGIC             <li><a href="https://www.kaggle.com/sermakarevich/sklearn-pipelines-tutorial">Sklearn pipelines tutorial</a></li>
# MAGIC             <li><a href="https://www.kdnuggets.com/2017/12/managing-machine-learning-workflows-scikit-learn-pipelines-part-1.html">Managing Machine Learning workflows with Sklearn pipelines</a></li>
# MAGIC             <li><a href="https://towardsdatascience.com/a-simple-example-of-pipeline-in-machine-learning-with-scikit-learn-e726ffbb6976">A simple example of pipeline in Machine Learning using SKlearn</a></li>
# MAGIC         </ul>
# MAGIC     </ul>
# MAGIC     <h1>Credits</h1>
# MAGIC     <ul>
# MAGIC         <li>To Brandon Foltz for his <a href="https://www.youtube.com/channel/UCFrjdcImgcQVyFbK04MBEhA">youtube</a> channel and for being an amazing teacher.</li>
# MAGIC         <li>To GA where I started my data science journey.</li>
# MAGIC         <li>To Kaggle community for inspiring me over and over again with all the resources I need.</li>
# MAGIC         <li>To Udemy Course "Deployment of Machine Learning". I have used and modified some of the code from this course to help making the learning process intuitive.</li>
# MAGIC     </ul>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC <div class="alert alert-info">
# MAGIC <h4>If you like to discuss any other projects or just have a chat about data science topics, I'll be more than happy to connect with you on:</h4>
# MAGIC     <ul>
# MAGIC         <li><a href="https://www.linkedin.com/in/masumrumi/"><b>LinkedIn</b></a></li>
# MAGIC         <li><a href="https://github.com/masumrumi"><b>Github</b></a></li>
# MAGIC         <li><a href="https://masumrumi.github.io/cv/"><b>masumrumi.github.io/cv/</b></a></li>
# MAGIC         <li><a href="https://www.youtube.com/channel/UC1mPjGyLcZmsMgZ8SJgrfdw"><b>Youtube</b></a></li>
# MAGIC     </ul>
# MAGIC 
# MAGIC <p>This kernel will always be a work in progress. I will incorporate new concepts of data science as I comprehend them with each update. If you have any idea/suggestions about this notebook, please let me know. Any feedback about further improvements would be genuinely appreciated.</p>
# MAGIC 
# MAGIC <h1>If you have come this far, Congratulations!!</h1>
# MAGIC 
# MAGIC <h1>If this notebook helped you in any way or you liked it, please upvote and/or leave a comment!! :)</h1></div>
