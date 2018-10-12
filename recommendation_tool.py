df=pd.read_csv('allproduct_df.csv')
df['corpus_no_brand_no_name']=df['Category'].astype(str).str.cat(df[['Ingredients','Description']].astype(str), sep=',')
tfidf_matrix_3 = TfidfVectorizer(stop_words='english').fit_transform(df['corpus_no_brand_no_name'])
cosine_sim_3 = cosine_similarity(tfidf_matrix_3, tfidf_matrix_3)
indices_3 = pd.Series(df.index, index=df['Name']).drop_duplicates()


def get_recommendations_no_brand_no_name_cs(Name, cosine_sim=cosine_sim_3):
    # Get the index of the product that matches the name
    idx = indices_3[Name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:10]
    product_indices = [i[0] for i in sim_scores]
    recommended_df=df[['Name', 'Brand', 'URL']].iloc[product_indices]
    return recommended_df

def recommendation_df(Name):
    rec = IFrame('hi.gif', width=700, height=300)
    if Name == "Hi There!":
        rec = IFrame('hi.gif', width=700, height=300)
    if Name == "":
        rec = IFrame('hi.gif', width=700, height=300)
    else:
        rec=get_recommendations_no_brand_no_name_cs(Name)
        print ('recommending...')
        rec_link_list=rec.URL.tolist()
        driver=webdriver.Chrome()
        driver.get(rec_link_list[1])
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/div/div/button").click()
    return rec

search_widget = widgets.Text(placeholder = 'Search product', description='Search:', disabled=False,continuous_update=False)
