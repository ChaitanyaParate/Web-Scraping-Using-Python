import requests
from bs4 import BeautifulSoup
import pandas

oyo_url = "https://www.oyorooms.com/search?location=Nagpur%2C%20Maharashtra%2C%20India&city=Nagpur&searchType=city&checkin=30%2F09%2F2023&checkout=01%2F10%2F2023&roomConfig%5B%5D=1&guests=1&rooms=1&filters%5Bcity_id%5D=43"

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' , 'Accept-Language': 'en-US'})

req = requests.get(oyo_url , headers=headers)

content = req.content

soup = BeautifulSoup(content, "html.parser")

all_hotels = soup.find_all("div" , {"class":"oyo-row oyo-row--no-spacing hotelCardListing"})

scraped_info_list = []

for hotels in all_hotels:
    hotel_dict = {}
    hotel_dict["Name"] = hotels.find("h3" , {"class": "listingHotelDescription__hotelName d-textEllipsis"}).text
    hotel_dict["Address"] = hotels.find("span" , {"itemprop":"streetAddress"}).text
    hotel_dict["Price"] = hotels.find("span" , {"class":"listingPrice__finalPrice"}).text
    
    try:
        hotel_dict["Rating"] = hotels.find("span", {"class": "hotelRating__ratingSummary"}).text
       
    except AttributeError:
        pass
    
    hotel_parent_amenity = hotels.find("div" , {"class":"amenityWrapper"})
    amenities_list = []
    
    for amenity in hotel_parent_amenity.find_all("div", {"class": "amenityWrapper__amenity"}):
        amenities_list.append(amenity.find("span" , {"class": "d-body-sm"}).text.strip())
        new_amenities_list = amenities_list[:-1]
        
        
    hotel_dict["Amenities"] = ','.join(new_amenities_list)
    
    scraped_info_list.append(hotel_dict)
        
    
    #print(hotel_name , hotel_address , hotel_prise , hotel_rating , new_amenities_list)
 
    
 
    
detaFrame = pandas.DataFrame(scraped_info_list)
detaFrame.to_csv("Oyo.csv")
    
 
    
 
    
 
    
 
    
 
    