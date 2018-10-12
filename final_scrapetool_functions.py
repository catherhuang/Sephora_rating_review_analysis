from bs4 import BeautifulSoup
import urllib3
import certifi
import requests
import pandas as pd
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import re
import json
import random


############
#pull product links from each of the catagory page
############

def make_soup_object(url):
    """make soup object for each page"""
    return BeautifulSoup(requests.get(url).content, "lxml")
def get_item_links(pg_soup):
    items=[]
    for item in pg_soup.findAll("a", class_='css-ix8km1'):
        items.append(item)
    item_urls=[]
    for i in items:
        item_urls.append(str("https://www.sephora.com"+ i.get('href')))
    return item_urls
def make_product_df(product_pages):
    """insert_all the page links from product"""
    all_products=[]
    for page in product_pages:
        all_products.extend(get_item_links(make_soup_object(page)))
    product_link_df=pd.DataFrame(data=all_products, columns=['url'])
    return product_link_df
def create_pages(category_url, last_pg_num):
    """input the category main page url to set limit to 12 items per page """
    page_lst=[category_url + "?pageSize=12"]
    for i in range(2, last_pg_num+1):
        page_lst.append(category_url + "?pageSize=12&currentPage=" + str(i))
    return page_lst
def clean_text (text):
    clean_1=text.replace('\r\n\r\n', '')
    clean_2=clean_1.replace('\u3000\r\n', '')
    clean_3=clean_2.replace('\r\n', '')
    clean_4=clean_3.replace('\u3000', '')
    clean_5=clean_4.replace('\n', '')
    clean_6=clean_5.replace("\'", '')
    clean_7=clean_6.lower()
    return clean_7

def make_product_id (product_soup):
    item_id=product_soup.find("link", rel="canonical").get('href')[-7:]
    return item_id


def product_info (product_url):

    """make product soup"""
    product_soup=make_soup_object(product_url)
    product_id=product_url.split("-")[-1]
    """define info for product data"""
    #find brand name
    brand=product_soup.find("span", class_='css-1lujsz0').text
    #find product name
    name=product_soup.find("span", class_='css-at8tjb').text
    #find product price(sale item will have original price )
    price=product_soup.find("div", class_="css-n8yjg7").text.split(' ')[0]
    #find product id
    #item_id=product_soup.find("link", rel="canonical").get('href')[-7:]
    #find product link
    link=product_soup.find("link", rel="canonical").get('href')
    #find details for the product
    details=product_soup.findAll("div", class_="css-1vwy1pm")[0].text
    #find ingredients for the product
    ingredients=product_soup.findAll("div", class_="css-1vwy1pm")[2].text

    reviews=product_soup.findAll("span", class_='css-mmttsj')[0].text
    likes=product_soup.findAll("span", class_='css-mmttsj')[1].text
    product_df=pd.DataFrame({'ID':[product_id],'Link':[link],
                             'Brand':[brand],
                             'Name':[name],
                             'Price':[price],
                             'Reviews':[reviews],
                             'Likes':[likes],
                             'Details':[clean_text(details)],
                             'Ingredients':[clean_text(ingredients)]})
    return product_df

def product_info_no_ing (product_url):
    """make product soup"""
    product_soup=make_soup_object(product_url)
    product_id=product_url.split("-")[-1]

    """define info for product data"""
    #find brand name
    brand=product_soup.find("span", class_="css-15zphjk").text
    #find product name
    name=product_soup.find("span", class_='css-r4ddnb').text
    #find product price(sale item will have original price )
    price=product_soup.find("div", class_="css-n8yjg7").text.split(' ')[0]

    #find product link
    link=product_soup.find("link", rel="canonical").get('href')
    #find details for the product
    details=product_soup.findAll("div", class_="css-192qj50")[0].text
    likes=product_soup.findAll("span", class_="css-rok4hb ")[1].text
    reviews=product_soup.findAll("span", class_="css-rok4hb ")[0].text
    try:
        ingredients=product_soup.findAll("div", class_="css-192qj50")[2].text
    except:
         ingredients=None
    product_df=pd.DataFrame({'ID':[product_id],
                            'URL':[link],
                             'Brand':[brand],
                             'Name':[name],
                             'Price':[price],
                             'Reviews':[reviews],
                             'Likes':[likes],
                             'Description':[clean_text(details)],
                             'Iingredients': [clean_text(ingredients)]})
    return product_df

def clean_text_ver2 (text):
    """clean html code from json"""
    text=str(text)
    _1=text.replace('\r\n\r\n', '')
    _2=_1.replace('\u3000\r\n', '')
    _3=_2.replace('\r\n', '')
    _4=_3.replace('\u3000', '')
    _5=_4.replace('\n', '')
    _6=_5.replace("\'", '')
    _7=_6.lower()





######################
#scrape tool for bazaarvoice api
######################


def create_product_api_requests(product_id):
    """use product id to make api request urls"""
    start_url='https://api.bazaarvoice.com/data/reviews.json?Filter=ProductId%3A'
    end_url='&Sort=Helpfulness%3Adesc&Include=Products%2CComments&Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4'
    request_url=start_url + product_id + end_url
    return request_url

def product_info_dict(api_url):
    """generate product info dictionary"""
    product_info_dict=json.loads(requests.get(api_url).content.decode("utf-8"))
    return product_info_dict

def star_rating_distribution(review_distribution):
    """clarify distribution of the number of stars for rating
        review distribution is a list from, starting w lowest star to highest star"""
    star_1=0
    star_2=0
    star_3=0
    star_4=0
    star_5=0
    for i in review_distribution:
        if i['RatingValue']==1:
            star_1+=i['Count']
        elif i['RatingValue']==2:
            star_2+=i['Count']
        elif i['RatingValue']==3:
            star_3+=i['Count']
        elif i['RatingValue']==4:
            star_4+=i['Count']
        elif i['RatingValue']==5:
            star_5+=i['Count']
    star_distribution=[star_1, star_2, star_3 , star_4, star_5]
    return star_distribution

def reviewer_info_distribution_skintype(product_context_distribtuion):
    skinType_normal=0
    skinType_combination=0
    skinType_dry=0
    skinType_oily=0
    if 'skinType' in product_context_distribtuion.keys():
        skin_type_distribution=product_context_distribtuion['skinType']['Values']
        for i in skin_type_distribution:
            if i['Value']=='normal':
                skinType_normal+=i['Count']
            if i['Value']=='combination':
                skinType_combination+=i['Count']
            if i['Value']=='dry':
                skinType_dry=+i['Count']
            if i['Value']=='oily':
                skinType_oily=+i['Count']

    skinTypes=[skinType_normal, skinType_combination,skinType_dry,  skinType_oily]
    return skinTypes

def reviewer_info_distribution_eyecolor(product_context_distribtuion):
    eyecolor_blue=0
    eyecolor_brown=0
    eyecolor_green=0
    eyecolor_hazel=0
    eyecolor_gray=0
    if 'eyeColor' in product_context_distribtuion.keys():
        eyeColor_distribution=product_context_distribtuion['eyeColor']['Values']
        for i in eyeColor_distribution:
            if i['Value']=='blue':
                eyecolor_blue+=i['Count']
            if i['Value']=='brown':
                eyecolor_brown+=i['Count']
            if i['Value']=='green':
                eyecolor_green+=i['Count']
            if i['Value']=='hazel':
                eyecolor_hazel+=i['Count']
            if i['Value']=='gray':
                eyecolor_gray+= i['Count']

    eyeColor=[eyecolor_blue, eyecolor_brown, eyecolor_green, eyecolor_hazel, eyecolor_gray]
    return eyeColor


def reviewer_info_distribution_skinconcerns(product_context_distribtuion):
    skinconcern_acne=0
    skinconcern_aging=0
    skinconcern_blackheads=0
    skinconcern_calluses=0
    skinconcern_cellulite=0
    skinconcern_cuticles=0
    skinconcern_darkCircles=0
    skinconcern_dullness=0
    skinconcern_pores=0
    skinconcern_redness=0
    skinconcern_sensitivity=0
    skinconcern_stretchMarks=0
    skinconcern_sunDamage=0
    skinconcern_unevenSkinTones=0

    if 'skinConcerns'in product_context_distribtuion.keys():
        skinConcerns_distribution=product_context_distribtuion['skinConcerns']['Values']
        for i in skinConcerns_distribution:
            if i['Value']=='acne':
                skinconcern_acne+=i['Count']
            if i['Value']=='aging':
                skinconcern_aging+=i['Count']
            if i['Value']=='blackheads':
                skinconcern_blackheads+=i['Count']
            if i['Value']=='calluses':
                skinconcern_calluses+=i['Count']
            if i['Value']=='cellulite':
                skinconcern_cellulite+= i['Count']
            if i['Value']=='cuticles':
                skinconcern_cuticles+= i['Count']
            if i['Value']=='darkCircles':
                skinconcern_darkCircles+= i['Count']
            if i['Value']=='dullness':
                skinconcern_dullness+=i['Count']
            if i['Value']=='pores':
                skinconcern_pores+=i['Count']
            if i['Value']=='redness':
                skinconcern_redness+=i['Count']
            if i['Value']=='sensitivity':
                skinconcern_sensitivity+=i['Count']
            if i['Value']=='stretchMarks':
                skinconcern_stretchMarks+=i['Count']
            if i['Value']=='sunDamage':
                skinconcern_sunDamage+=i['Count']
            if i['Value']=='unevenSkinTones':
                skinconcern_unevenSkinTones+=i['Count']
    skinconcerns=[skinconcern_acne,skinconcern_aging,skinconcern_blackheads,skinconcern_calluses,skinconcern_cellulite, skinconcern_cuticles,skinconcern_darkCircles, skinconcern_dullness, skinconcern_pores,skinconcern_redness,skinconcern_sensitivity,skinconcern_stretchMarks,skinconcern_sunDamage,skinconcern_unevenSkinTones ]
    return skinconcerns

def reviewer_info_distribution_hairColor(product_context_distribtuion):
    haircolor_blonde=0
    haircolor_brunette=0
    haircolor_auburn=0
    haircolor_black=0
    haircolor_red=0
    haircolor_gray=0
    if 'hairColor' in product_context_distribtuion.keys():
        hairColor_distribution = product_context_distribtuion['hairColor']['Values']
        for i in hairColor_distribution:
            if i['Value']=='blonde':
                haircolor_blonde+=i['Count']
            if i['Value']=='brunette':
                haircolor_brunette+=i['Count']
            if i['Value']=='auburn':
                haircolor_auburn+=i['Count']
            if i['Value']=='black':
                haircolor_black+=i['Count']
            if i['Value']=='red':
                haircolor_red+=i['Count']
            if i['Value']=='gray':
                haircolor_gray+=i['Count']
    hairColors=[haircolor_blonde,haircolor_brunette, haircolor_auburn,haircolor_black,haircolor_red, haircolor_gray]
    return hairColors

def reviewer_info_distribution_skintone(product_context_distribtuion):
    skintone_fair=0
    skintone_light=0
    skintone_medium=0
    skintone_olive=0
    skintone_deep=0
    skintone_dark=0
    skintone_porcelain=0
    skintone_tan=0
    skintone_ebony=0
    if 'skinTone' in product_context_distribtuion.keys():
        skinTone_distribution = product_context_distribtuion['skinTone']['Values']
        for i in skinTone_distribution:
            if i['Value']=='fair':
                skintone_fair+=i['Count']
            if i['Value']=='light':
                skintone_light+=i['Count']
            if i['Value']=='medium':
                skintone_medium+=i['Count']
            if i['Value']=='olive':
                skintone_olive+=i['Count']
            if i['Value']=='deep':
                skintone_deep+=i['Count']
            if i['Value']=='dark':
                skintone_dark+=i['Count']
            if i['Value']=='porcelain':
                skintone_porcelain+=i['Count']
            if i['Value']=='tan':
                skintone_tan+=i['Count']
            if i['Value']=='ebony':
                skintone_ebony+=i['Count']
    skinTones=[skintone_fair,skintone_light,skintone_medium,skintone_olive,skintone_deep,skintone_dark,skintone_porcelain,skintone_tan,skintone_ebony ]
    return skinTones

def reviewer_info_distribution_age(product_context_distribtuion):
    age_13to17=0
    age_18to24=0
    age_25to34=0
    age_35to44=0
    age_45to54=0
    over54=0
    if 'age' in product_context_distribtuion.keys():
        age_distribution = product_context_distribtuion['age']['Values']
        for i in age_distribution:
            if i['Value']=='13to17':
                age_13to17+=i['Count']
            if i['Value']=='18to24':
                age_18to24+=i['Count']
            if i['Value']=='25to34':
                age_25to34+=i['Count']
            if i['Value']=='35to44':
                age_35to44+=i['Count']
            if i['Value']=='45to54':
                age_45to54+=i['Count']
            if i['Value']=='over54':
                over54+=i['Count']
    ages=[age_13to17,age_18to24,age_25to34,age_35to44,age_45to54,over54]
    return ages

def product_info_df(product_id):
    """use create product api to create api links from id, then create dictionary of product info"""
    product_dict=product_info_dict(create_product_api_requests(product_id))
    """extract info from the product info dict """
    api_id=product_dict['Includes']['ProductsOrder'][0]
    product_url=product_dict['Includes']['Products'][api_id]['ProductPageUrl']
    product_name=product_dict['Includes']['Products'][api_id]['Name']
    product_description=product_dict['Includes']['Products'][api_id]['Description']
    product_brand=product_dict['Includes']['Products'][api_id]['Brand']['Name']
    number_of_reviews=product_dict['TotalResults']
    #details from the review stats
    review_stats=product_dict['Includes']['Products'][api_id]['ReviewStatistics']
    recommended_count=review_stats['RecommendedCount']
    not_recommend_count=review_stats['NotRecommendedCount']
    average_rating=review_stats['AverageOverallRating']
    review_distribution = review_stats['RatingDistribution']
    rating_breakdown= star_rating_distribution(review_distribution)
    product_context_distribtuion=review_stats['ContextDataDistribution']
    skintype=reviewer_info_distribution_skintype(product_context_distribtuion)
    eyecolor=reviewer_info_distribution_eyecolor(product_context_distribtuion)
    skinconcerns=reviewer_info_distribution_skinconcerns(product_context_distribtuion)
    haircolor=reviewer_info_distribution_hairColor(product_context_distribtuion)
    skintone=reviewer_info_distribution_skintone(product_context_distribtuion)
    ages=reviewer_info_distribution_age(product_context_distribtuion)
    first_review_date=pd.to_datetime(review_stats['FirstSubmissionTime'])
    product_info_df=pd.DataFrame({'ID':[product_id ],
                                  'dictID':[api_id],
                                  'URL': [product_url],
                                  'Brand':[product_brand],
                                  'Name':[product_name],
                                  'Reviews':[number_of_reviews],
                                  'RecommendedCount':[recommended_count],
                                  'NotRecommendCount':[not_recommend_count],
                                  'AverageRating':[average_rating],
                                  'FirstReviewDate':[first_review_date],
                                  '1StarCount':[rating_breakdown[0]],
                                  '2StarCount':[rating_breakdown[1]],
                                  '3StarCount':[rating_breakdown[2]],
                                  '4StarCount':[rating_breakdown[3]],
                                  '5StarCount':[rating_breakdown[4]],
                                  'skinType_normal':[skintype[0]],
                                  'skinType_combination':[skintype[1]],
                                  'skinType_dry':[skintype[2]],
                                  'skinType_oily':[skintype[3]],
                                  'eyecolor_blue':[eyecolor[0]],
                                  'eyecolor_brown':[eyecolor[1]],
                                  'eyecolor_green':[eyecolor[2]],
                                  'eyecolor_hazel':[eyecolor[3]],
                                  'eyecolor_gray':[eyecolor[4]],
                                  'skinconcern_acne':[skinconcerns[0]],
                                  'skinconcern_aging':[skinconcerns[1]],
                                  'skinconcern_blackheads':[skinconcerns[2]],
                                  'skinconcern_calluses':[skinconcerns[3]],
                                  'skinconcern_cellulite':[skinconcerns[4]],
                                  'skinconcern_cuticles':[skinconcerns[5]],
                                  'skinconcern_darkCircles':[skinconcerns[6]],
                                  'skinconcern_dullness':[skinconcerns[7]],
                                  'skinconcern_pores':[skinconcerns[8]],
                                  'skinconcern_redness':[skinconcerns[9]],
                                  'skinconcern_sensitivity':[skinconcerns[10]],
                                  'skinconcern_stretchMarks':[skinconcerns[11]],
                                  'skinconcern_sunDamage':[skinconcerns[12]],
                                  'skinconcern_unevenSkinTones':[skinconcerns[13]],
                                  'haircolor_blonde': [haircolor[0]],
                                  'haircolor_brunette':[haircolor[1]],
                                  'haircolor_auburn':[haircolor[2]],
                                  'haircolor_black':[haircolor[3]],
                                  'haircolor_red':[haircolor[4]],
                                  'haircolor_gray':[haircolor[5]],
                                  'skintone_fair':[skintone[0]],
                                  'skintone_light':[skintone[1]],
                                  'skintone_medium':[skintone[2]],
                                  'skintone_olive':[skintone[3]],
                                  'skintone_deep':[skintone[4]],
                                  'skintone_dark':[skintone[5]],
                                  'skintone_porcelain':[skintone[6]],
                                  'skintone_tan':[skintone[7]],
                                  'skintone_ebony':[skintone[8]],
                                  'age_13to17':[ages[0]],
                                  'age_18to24':[ages[1]],
                                  'age_25to34':[ages[2]],
                                  'age_35to44':[ages[3]],
                                  'age_45to54':[ages[4]],
                                  'over54':[ages[5]],
                                  'Description':[product_description]})
    return product_info_df

def create_api_product_info(product_id_list):
    """input product id, and using product info to organize json into df"""
    product_df=pd.DataFrame()
    bad_id=[]
    for i in product_id_list:
        try:
            product_df=product_df.append(product_info_df(i))
        except:
            bad_id.append(i)
            pass

##############
##SELENIUM WEB DRIVER for review info
##############

def scroll_and_grab_review_info(product_url, driver):
    """use selenium (Chrome webdriver) to interact with individual product page
    scroll and activate the load more section to pull review info  """
    #driver=webdriver.Chrome()
    driver.get(product_url)
    while True:
        try:
            cancel_button=driver.find_element_by_class_name("css-ll28en")
            cancel_button.click()
        except(NoSuchElementException, StaleElementReferenceException):
            break

    element = driver.find_element_by_class_name('css-gf5e4e')
    element.location_once_scrolled_into_view
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 1000);")
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 1800);")
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 800);")
    driver.implicitly_wait(10)
    element=driver.find_element_by_xpath('//*[@id="ratings-reviews"]/div[2]/div[1]/div[1]/span')
    element.location_once_scrolled_into_view
    while True:
        try:
            time.sleep(5)
            button=driver.find_element_by_class_name("css-end8gr")
            button.click()
        except:
            break
    total_reviews=driver.find_element_by_class_name('css-ank82h').text.split(' ')[0]

    #number of 5 star review
    star_5_path='//*[@id="ratings-reviews"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[3]'
    star_5=driver.find_element_by_xpath(star_5_path).text

    #number of 4 star review
    star_4_path='//*[@id="ratings-reviews"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[3]'
    star_4=driver.find_element_by_xpath(star_4_path).text

    #numner of 3 star review
    star_3_path='//*[@id="ratings-reviews"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[3]/td[3]'
    star_3=driver.find_element_by_xpath(star_3_path).text

    #number of 2 star review
    star_2_path='//*[@id="ratings-reviews"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[4]/td[3]'
    star_2=driver.find_element_by_xpath(star_2_path).text

    #number of 1 star review
    star_1_path='//*[@id="ratings-reviews"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[5]/td[3]'
    star_1=driver.find_element_by_xpath(star_1_path).text

    #avg review score:
    avg_review=driver.find_element_by_class_name('css-ffj77u').text

    rr_stats=driver.find_element_by_class_name('css-z1ro2e').text
    #name of reviewers
    # reviewer_name=driver.find_elements_by_class_name('css-s5vrlh')
    # reviewer_name_lst=[reviewer.text for reviewer in reviewer_name]
    #find reviewer info
    reviewer_info=driver.find_elements_by_class_name('css-1ov92f')
    reviewer_info_lst=[info.text for info in reviewer_info]


    #find numbers of star for each review:
    review_stars_path=['//*[@id="ratings-reviews"]/div[2]/div[3]/div[{}]/div[2]/div[2]/div[1]/div[1]/div/div[2]'.format(str(i)) for i in range(1,int(total_reviews)+1)]
    review_stars_lst=[]
    for path in review_stars_path:
        review_stars_lst.append(driver.find_element_by_xpath(path).get_attribute('style'))

    #find review text
    review_text=driver.find_elements_by_class_name('css-t3xto5')
    review_text_lst=[tx.text for tx in review_text]

    review_stats=pd.DataFrame({'product id': [product_url[-7:]],
                           'number of reviews':[total_reviews],
                           'number of 5 star reviews':[star_5],
                           'number of 4 star reviews':[star_4],
                           'number of 3 star reviews':[star_3],
                            'number of 2 star reviews':[star_2],
                            'number of 1 star reviews':[star_1],
                            'avg review':[avg_review]})
    reviews_df=pd.DataFrame({'product_id':product_url[-7:],
                      'reviewers':[i.split('\n')[0] for i in reviewer_info_lst],
                         'reviewer info': [i.split('\n')[1:] for i in reviewer_info_lst],
                        'reviewer stars':[i.split('width: ')[1] for i in review_stars_lst],
                        'review text':[i.split('\n')[1:] for i in review_text_lst],
                        'review date': [i.split('\n')[0] for i in review_text_lst],
                        'review_helpful': [i.split('\n')[-1] for i in review_text_lst],
                        'review_not_helpful':[i.split('\n')[-2] for i in review_text_lst]})

    return review_stats, reviews_df

# create separate df for review and stats, incorporate selenium function to pull necessary info
driver=webdriver.Chrome()
prod_reveiw_stats=pd.DataFrame()
prod_review_info=pd.DataFrame()
for url in skincare_links:
    try:
        prod_reveiw_stats=prod_reveiw_stats.append(scroll_and_grab_review_info(url, driver)[0])
        prod_review_info=prod_review_info.append(scroll_and_grab_review_info(url, driver)[1])
    except:
        pass
