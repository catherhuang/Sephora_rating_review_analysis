# Sephora Rating and Review Analysis

# Goal: 
My overarching goal for the project is to be able to utilize machine learning to make predictions on product rating and recommendation based on that product's customer profiles, or the description and ingredients. With a working model, users can input profile information about the product, or the ingredients and description of the product, and the model can predict if customers will recommend that product, or if the product's average rating will be above or below average compared to the other products on Sephora's website. Having the ability to make predict will allow the retailers to pre-determine product performance (at least on the product's rating or recommendation level). The beauty retail market is a $250 billion global business, roughly 56 billion in the US. However, the industry is also competitive and fast-paced, therefore, for a brand/store to carry a popular product, where its highly rated and reviewed, and has a strong customer base, is an interesting area to explore.

# Data Processing: 
Utilizing the dataset from Sephora.com, the dataset contains the product's name, description, brand, ingredients (if available), category, average rating, number of recommendations, as well as the reviewers' profile (eye color, hair color, skincare concern, skin type etc), as well as the breakdown of review information (number of recommendations, star count). These are going to be all the available features in which I will be able to use to help make a prediction. 

# Data Exploration: 

### Star count by product category 
<p align="center">
  <img src="final_project_img/star_count.png" title="star count by category">
</p>
By analyzing the star count for each of the product category, each of the categories has an overwhelmingly high number of products with 5-star counts. Therefore, any products that do not have an average review of 4 stars or above (4 star is the average review for all the products on Sephora.com) will be labeled as performing below average, and any product with an average review of 4 stars or above will be labeled as performing above average. 

### Product recommendation by category 
The chart below shows the break down of the different product categories carried by the company's website, it also shows that the majority of the reviewers will more likely recommend that product being reviewed. As a target for regression analysis, it will be interesting to be able to determine the percentage of customers will recommend the products. A higher percentage of people recommend a product is a good determination of the product's performance, as most people make purchases based on recommendations from their peers. 
<p align="center">
  <img src="final_project_img/recommendation_pie_chart.png" title="recommendation % by product type ">
</p>

### Customer profile review 
The boxplot visualizations of the reviewer profiles are broken down by product category. The boxplots help show the most common profile types of the reviewers on Sephora.com. According to the simple analysis, these customers are mostly between the age range of 24-35, have brown hair, brown eyes, combination skin type, and have skin concerns related to acne or aging. The profile of the product determines the audience in which that product is targeting. 
<p align="center">
  <img src="final_project_img/Screen Shot 2018-10-12 at 6.42.32 PM.png" title="customer profiles">
</p>

### Price breakdown by product types
The graph below shows that Sephora mainly keeps their products at around the same price range of $30-50. 
<p align="center">
  <img src="final_project_img/price_png.png" title="price breakdown by category">
</p>

### Feature correlation
By analyzing if there are any significant correlation of my remaining features, I can avoid multicollinearity, in which a one predictor variable in a multiple regression model can be linearly predicted from the others with a substantial degree of accuracy. According to the correlation map below, the price has a slightly negative impact on rating, however, a regression analysis using price as my only feature created a poor model that failed to perform better than random guessing. 
<p align="center">
  <img src="final_project_img/correlation_map.png" title="feature correlation">
</p>

# Regression Analysis (using customer profiles to predict if customers will recommend a product) 
### GradientBoostingRegressor(n_estimators=400, max_features='sqrt') 
Using gradient boosting regressor, the model is able to make a relatively accurate prediction on the percentage of users who will recommend a product using features based on customer profiles. The strongest feature in help determining the recommendation is price according to the algorithm. 
<p align="left">
  <img src="final_project_img/recommendation_regression.png" title="recommendation prediction">
  <img src="final_project_img/feature_importance_regression.png" title="recommendation prediction">
</p>

# Classification Analysis 
### Using customer profiles to predict if a product's rating will be above or below average
### AdaBoost classifier(n_estimators=150)
Using AdaBoost classifier, I tried to predict that give the customer profile of a product, if a product will have an above average or below average rating. The model is good at making a true positive prediction of a product performing above average, however, it has a poor performance at making an accurate prediction at a product performing below average.
<p align="left">
  <img src="final_project_img/rating_model_profiles.png" title="rating prediction cm">
  <img src="final_project_img/profiles_model_report.png" title="rating prediction report">
</p>

### Using product description and ingredients to predict if a product's rating will be above or below average
Also note, to reduce the high dimensionality of vectorized text data, features are limited to the top 900 words under TFIDF vectorization. Multiple regularizations were tested, however, limiting features was the most effective method in this instance. 

### MultinomialNB(alpha=10)
Using a Naive Bayes Multinomial classifier, and using the product description as my features, the model has a more balanced performance. 

<p align="left">
  <img src="final_project_img/rating_model_text.png" title="rating prediction cm text">
  <img src="final_project_img/rating_model_text_report.png" title="rating prediction report text">
</p>

### Deep Learning 
For features that are complex, I also tried a deep learning approach to see if the model will be able to better capture the context of the description and the ingredients, and make a better prediction on rating performance. Although the deep learning model performs better at around 64% accuracy, the model is easily overfitted, its performance peaked at around 8 epochs. 
<p align="left">
  <img src="final_project_img/dl_model_epochs.png" title="epochs">
  <img src="final_project_img/dl_model.png" title="dl model">
</p>

# Bonus - Recommendation Engine
I was also able to leverage the rich text data to create a recommendation engine based on the product's ingredient and description as my corpus. The recommendation is demonstrated below, the first item listed is the product searched, and the remaining are products recommended by the engine. The recommendation  Additionally, I've incorporated selenium web browser to automatically pull up the link to the product most highly recommended. 
<p align="left">
  <img src="final_project_img/Screen Shot 2018-10-12 at 7.27.07 PM.png" title="epochs">
</p>


# Next Steps: 
* break down prediction by the product categories 
* cluster client types for each of the product, and use the clustered customer features to improve prediction
* analysis on why certain products do not perform well
* create a recommendation engine that also incorporates a price component 








