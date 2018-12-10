# City Recommendation in the USA using Yahoo Flickr Creative Commons 100M Dataset
### by Anant Jain, Ahmet Salih Gundogdu
### DS 5500 Fall 2018 --- Prof. Cody Dunne, Northeastern University

## Motivation:

While the procession of transportation industry in the last hundred years enabled more travelling options to the people, it wasn't until just half a decade ago that the egression of social media platforms, shared thriftiness and GPS equipped mobile phones enabled these digital footprints of human mobility to be available publicly to the entire world. In this new world of shared economy, travelling cost per person has reduced due to which more and more people are moving from one region to another leaving behind their digital trails on social media sites. Although it might be still unclear about how continuing our online existence is going to affect the future of the human race, one thing is for certain that all this data that we are producing every day, exemplifies an inexhaustible resource which can be utilized for innumerous scientific studies.

The geo-location part of travel check-ins allows researchers to concentrate their focus on regions like populated cities.More than half of the population of the entire world resides in them. However, these cities aren't studied just because a lot of people live in them, but also because they have a rich history of development and growth, which lures many travelers and tourists from all over the world.

In this era of social networking sites, people's behavior online could help us have an idea about their tastes and preferences. Social check-ins, which store geo-tagged information about users, can be utilized by researchers and businesses to investigate these preferences and improve their services. In this project, we utilize the travel check-in data and use data-based visualizations to explore, assess and evaluate multiple SVD algorithms for the purposes of identifying anomalies, generating trust and providing the best recommendation for cities to visit in the USA.

## Data:

We are using Yahoo Flickr Creative Commons (YFCC100M) dataset which is known to be one of the largest assemblages of multimedia check-ins ever created. It is publicly hosted on AWS and was released under the YahooWeb-Scope program. It comprises of hundred million media objects dating between 2004 and 2014. Each line contains the metadata for one media object. Themetadata is cut and tab-separated into following field names: media identifier, user identifier, date taken, date uploaded, capture device, location (longitude & latitude, if available), accuracy and Creative Commons license it was published under. In addition, metadata fields like object title, machine tags, user tags, media description and a link from where the media object can be downloaded are listed.

We pruned the data first by eliminating unwanted columns in order to make it workable with limited RAM; and then by omitting records that weren't geo-tagged (i.e. more than 50%). Since we are focusing the study only on the cities in the US, we further filtered the data to records checked in the US. To do so, an expansion of YFCC100M containing the reverse geocode information of all records was utilized. After both pruning and merging, we were left with about 16 million records and the following set of columns.

| Column        | Description                                                          | Data Type    |
|---------------|----------------------------------------------------------------------|--------------|
| pid           | Unique media identifier                                              | categorical  |
| user_nickname | User identifier                                                      | categorical  |
| date_taken    | Date the media object was created                                    | ordinal      |
| longitude     | Longitude of the location the media object was checked at.           | quantitative |
| latitude      | Latitude of the location the media object was checked at.            | quantitative |
| url           | Link from where the media object can be downloaded                   | categorical  |
| town          | City the media object was checked in, extracted from address column  | categorical  |
| state         | State the media object was checked in, extracted from address column | categorical  |

## Data Analysis:

#### Visualization 1: Check-ins hex-binned by location on Map

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_001.jpg)

The above visualization shows a hex-binned map of a sample of data. Hex-bins are used to encode location of check-ins and color is used to encode number of check-ins in that area. We see most of the check-in concentration is around cities like New York and San Francisco. The middle of the US has the least number of check-ins. It seems most of the popular cities which users like to travel to are situated on the coasts of the US.

#### Visualization 2: Top-10 Cities in Specified Date Range

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_002.jpg)

The above visualization shows an area chart which encodes date data on the x axis and number of check-ins on the y axis; accompanied by a bar chart which encodes the top-10 cities on the y-axis and number of check-ins on the x-axis in the specified date range. We clearly see the leading cities across the US.

Fun-fact: As we can see in the chart below, before 2010, the difference in the number of check-ins between that of New York and San Francisco isn't that much. But, after 2010, We see New York almost doubled it's count of check-ins and became the sole most popular city in the US.

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_003.png)

## Task Analysis:

| Priority | Domain Task                                                                                                      | Analytic Task | Search Task | Analyze Task |
|----------|------------------------------------------------------------------------------------------------------------------|---------------|-------------|--------------|
| 3        | Examining and evaluating the model performance of the recommended places against the given user’s travel history | Compare       | Locate      | Present      |
| 2        | Generate a ranked list of recommendations                                                                        | Sort          | Explore     | Present      |
| 1        | Visualize different models and hyperparameters for assessment of the best set of modeling parameters to use.     | Compare       | Explore     | Discover     |
| 4        | Exploratory Data Analysis                                                                                        | Compare       | Explore     | Discover     |

Our visualizations will be primarily developed for "discover" (i.e., exploratory visualizations), "present" (i.e., communicative visualizations) consumptions. These domain tasks will enable our potential users to have more understanding and flexibility of choosing different models for the location recommendation task. More on why we chose the specified tasks are as follows:
1. Index #4: As the model will predict the given user's tendencies as a number, we will be sorting the top 10 locations rather than calculating the proximity to the real location. Here we will evaluate our model performance using Precision@10 metric which is looking at the user's top ten location preference and predicted top 10 recommendations.
2. Index #3: Physically demonstrate and deliver the models’ outputs to the user.
3. Index #2: Enable user to choose their modeling approach (at least 2 different SVD adaptations) and tune their parameters and evaluation metric.
4. Index #1: Get an idea about the data on which all the analysis is based on.

The users of the end product will be researchers and machine learning engineers who are interested in recommendation systems, but the UI is going to be designed in such a way that a normal traveler who want some good recommendations could also make use of the tool.

## Model Description:

We give the user the freedom to assess and visualize different adaptations of SVD on his/her selection of hyperparameters.

We have the following options for Hyperparameter Testing and Model Selection:

Preprocessing:
1. Numeric: Counts the number of check-ins for each city per user and creates a numeric label in domain [0, inf).
2. Binary: Labels the user-location pair as 1 if user has checked-in in that city, else 0.

Models:
1. SVD_explicit: Use Singular Value Decomposition to extract user and location features and approximate the missing user check-ins by matrix factorization.
2. SVD_implicit: Use Singular Value Decomposition to extract user and location features and then apply Alternating Least Squares method to get an optimal fit for missing points.
Python libraries: Scipy, Scikit-learn, Pandas, Numpy, Implicit (Bold texts represents the packages used for building ML models)

Latent Dimensions: Denotes the number of dimensions/features to extract for each user and location.

Metric:
1. Precision-Train Set: Use Precision@10 metric which looks at the user's top 10 location preferences and compare it with the predicted top 10 recommendations for the Train Set.
2. Recall-Train Set: Use Recall as metric to assess the user's top 10 location preferences and compare it with the predicted top 10 recommendations for Train Set.
3. Precision-Validation Set: Use Precision@10 metric which looks at the user's top 10 location preferences and compare it with the predicted top 10 recommendations for the Validation Set.
4. Recall-Validation Set: Use Recall as metric to assess the user's top 10 location preferences and compare it with the predicted top 10 recommendations for the Validation Set.

## Design Process:

We started with drawing up some preliminary sketches based on our tasks. As it can be seen we were planning to have point and polygon layers on the EDA map initially. But we soon realized how over plotted it is going to look giver our dataset size. Polygon layers were supposed to the fix for that but they didn’t help much either if the user changed the level of the map. We experimented and researched on what would be the best encoding for the job and we settled with hex-bin layers.

Hyperparameter Testing was implemented exactly as planned at the initial stage. But, for Model Selection, as per the feedback we got from the instructors, we decided to change from box-plots to violin plots.

The biggest changes were made to the Evaluation and Results visualizations. We decided to drop Feature importance graph and integrate everything else on one big map. This resulted in a much cleaner UI design.

Preliminary Sketches:

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_004.png)
![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_005.png)

Digital Sketches:

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_006.png)
![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_007.png)

## Final Visualization:

We decided to divide our final Visualization into three sections:
1. Exploratory Data Analysis
2. Hyperparameter Testing & Model Selection
3. Evaluation and Results

Each section took care of at least one task in our tasks table. All the three section are comprised in a Bootstrap UI with a main panel and a side-bar panel.

We’ll go by each section and discuss its purpose, design justification and packages utilized for coding.

Exploratory Data Analysis:

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_008.png)

Exploratory Data Analysis is the first tab on the UI.
The main panel shows an interactive leaflet map with hex-binned layers. The position of the hex-bins ideally encodes location of the aggregated check-ins at each zoom level of the map. The color of the hex-bins encodes the number of check-ins in that aggregated region. A Green-Blue color scale from ColorBrewer is used. A user can investigate the number of check-ins contained in each hexagon by hovering the mouse pointer over the hexagon (this is going to show a tipsy tooltip).

The side-bar panel consists of an area chart and a bar chart made using D3. The area chart encodes the number of check-ins on the y-axis and check-in dates on the x-axis. This chart can be brushed and is linked to the map and the bar chart. Meaning, a user can filter the data shown by the visualizations on the page by date just by brushing the area chart. The bar chart encodes the top 10 checked-in cities/towns on the y-axis and the number of check-ins on the x-axis. As it is linked to the area chart, it updates accordingly with respect to the brushed date-range.

Hyperparameter Testing & Model Selection

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_009.png)

Hyperparameter Testing & Model Selection is the second tab on the UI.

The main panel is divided into two parts. First shows a multi-columned line chart to explore hyperparameter test results. The y-axis encodes the metric to evaluate the hyperparameters on and the x-axis encodes the latent dimensions of user’s choice. The column encodes the type of model for which the user wants to view the test results on. Second shows a violin plot encoding the metric on y-axis and model on x-axis. Area inside the violin denotes the distribution of metric for different latent dimensions chosen by the user. The color for both the chart encodes the types of preprocessing the user has chosen. All the visualizations in this section were made using plotly.

The side-bar panel has bootstrap and multi-select input elements so that the user can input his/her’s set of hyperparameters and models to explore and assess. Once the user hits the train button, the page makes a request to the flask server to get the data for the visualizations and show the best set of hyperparameters for entered inputs in the sidebar. The page fires a request to the get the data for default parameters when the user first switches to the tab.

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_010.png)

It might take some time for the page to receive the data from the server therefore a user is going to see the UX gif in the main panel. A loading hexagonal gif means the page has fired up a query to the server and is fetching the data for the visualization.

Evaluation and Results

![alt text](https://github.com/asgundogdu/locationRec/blob/master/documentation/Readme/Image_011.png)

Lastly, we have Evaluation and Results on the third tab of the UI.

The main panel shows an interactive leaflet map with animated uncopyrighted icons to encode visited towns (scenery gif) and recommended towns (compass gif) with details-on-demand hover functionality.

The side-bar panel accommodates the input elements for the final set of parameters the user wants his recommendations to be based on and a ranked list of results/recommendations for a random user which automatically gets selected from the database.

## Conclusion:

The overall goal of this project was to utilize the travel check-in data and use data-based visualizations to explore, assess and evaluate multiple SVD algorithms for the purposes of identifying anomalies, generating trust and providing the best recommendation for cities to visit in the US. Although using Singular Value Decomposition for Recommendation Systems is a fairly common approach; using visualizations to tune the hyperparameters of these models in real time and making the user a part of the machine learning process helps him/her to develop confidence in the results. While visualizations can be appealing and persuasive, it is important to have the proper visual encodings to use in the visualizations otherwise instead of making the user build trust in the results, they could easily push the user away.

Even though this project was a simple implementation of recommendation systems using Singular Value Decomposition, it can be scaled to integrate much complex deep-learning models designed for the tasks of collaborative filtering (i.e. Auto-Encoders). In addition to integration of complex models, distance-based evaluation techniques, where the results are evaluated on the basis of the gap between predicted recommendations and ground truth, are also suitable for future work.

## Evaluation Plan

In order to implement this designed system into the wild (real-time in real-world), we should perform an evaluation plan to measure the functionality, effectivenesss, efficiency, usability and usefullnesss of the the city recommendation system [source](http://www.wikiviz.org/wiki/Information_Visualization_Evaluation/). 

First all of the evaluations should be offline and as simulations (using streaming existing data, take a look at different time splits for training and test sets.) This will basically enable us to see the model's robustness for the changing data and also it will demonstrate that how frequently we should suppose to retrain the model. All of this offline evaluations should require around 5%-10% of the money we planned to spend on evaluation plan.

After we did 1-3 iterations on the offline evaluation plan, the difficult and expensive part is to deal with wild environment (online testing/beta testing).

There can be 10% of money can be spend on understanding the environment and work practive for this task. First, the targeted users will be data companies who are interested in inferring city recommendations for people who provides their historical locations. In this project, we proved that we can recommend users related/interesting cities that they are likely to visit in future; however it was not proven using other domains such as Instagram, Reddit, FourSquare etc. To test whether the trained model using YFCC100M data set can recommend related/interesting cities for other domain when the other social platform's data is utilized, we can build a controlled test scenerios to evaluate the precision@10 and recall@10 values in this additional datasets. Then, the effectiveness of the product become more evindent and can be regularized if there is need based on the performance in this evaluation setup. Furthermore, this will enable us to understand YFCC100M data's predictive power in other platform.

Also, for evaluating the system response time, we should first invest more on code optimization then evaluate the performance using different kind of devices (mobile, PC, etc.) and locations all over the world which can overall requires %10 of money that we hold for the evaluation task.

To understand visual reasoning, we want to quantitatively measure users engagement within our website. To do this we can apply A/B testing (Controlled Experiment [Munzer]) for N number of different visualization and monitor their engagements such as lenght of staying in the website, number of clicks and so on (5% of money can be spend). In the end of the evaluation, we can chose the best k (k<<N) number of visualization to be evaluated qualitatively as in below:

To qualitatively evaluate this application we can perform a wide usability tests including 100 people and can design a survey to understand tool's limitations based on the audiences' feedbacks. We can perform this evaluation using [Amazon Mechanical Turk](https://www.mturk.com/) where it is a crowdsourcing Internet marketplace and also enables individuals to publish and get answers for the surveys on specific tasks which can require %5 percentage of the monet can be spend in this evaluation plan. To take this qualitative evaluation further steps, we can use web applications and visualization experts to evaluate this product which will results more expensive than the other usability test (10% of money can be spend)); yet might be really effective to get experts' feedbacks on it. Moreover, this two usability testing tasks should be done in chronological order as after the quantitative evaluation, we apply surveys and expert evaluation. As the MTurk survey will cost less money, we can easily afford to do it multiple times when it was compared to the expert usability test.

We can iterate the whole online evaluation plans twice to meet the user expectations better (will cost almost around the same amount). In this respect, the whole evaluation plan will cost more or less the planned amount in the beginning. 

[slide](https://drive.google.com/file/d/1DMlpMktzxgSolNpbMLVaPc9z6wC6BNzY/view)

## Github Page
https://asgundogdu.github.io/locationRec/

## Github Repository
https://github.com/asgundogdu/locationRec
