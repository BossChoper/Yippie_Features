import requests
from bs4 import BeautifulSoup

def scrape_comments(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all <p> tags (adjust selector if comments have a specific class)
        comments = [p.get_text(strip=True) for p in soup.find_all('p')]
        return comments if comments else None
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    target_url = "https://www.restaurantji.com/dc/washington/donut-run-/comments/"
    comments = scrape_comments(target_url)
    
    if comments:
        print(f"Found {len(comments)} comments:")
        for idx, comment in enumerate(comments, 1):
            print(f"{idx}. {comment}")
    else:
        print("No comments found or scraping failed.")

""" Example output from Restaurantji, which gets comments from google and stores on webpage under <p> tags
Found 57 comments:
1. 6904 4th St NW, Washington(202) 506-3264Menu
2. OVERHYPED!Don’t get me wrong, the donuts here are amazing but for the HUGE lineups and also for it to be sold out before 2pm is a bit extreme!Donuts are  $3-4 each but it’s GIGANTIC! So I see the value, it’s fresh, ingredients are fresh, and you can check their instagram daily to see whats on their menu before coming.I personally don't like waiting just to get desserts, for $3-4 donuts? I just can't do it lol! i feel like they should have more donuts and longer hours.SO LETS GET TO IT!service: quick and fast, genericinterior: small and cute, i saw their packaging have art on the pink boxes on display , but my box was just plain pinkmenu: we got 12 donuts. Our fav was payday (has nuts, chocolates and cream in the middle), and creme brulee (which was unique and tastes like creme brulee) the other 10 donuts tasted generic or weird. SUPEE sweet but rhe dough isnt which is nice.price: its HUGE and they are generous with the toppings so its worth the $3-4overall: the experience of just getting donuts makes me not want to come back. i felt like it was overhyped.  its huge donuts with lots of toppings which you technically can get anywhere.Details: came here on a Sunday at 10:30am, you can literally see everybody with a pink box around loool
3. Atmosphere: 5
4. Food: 4
5. Service: 3
6. Like Donut Run needs another 5 star rating. Right?!  Well, here’s another one! They’re right!  Don’t run, sprint to Donut Run! The more you sprint, the more of them you can eat! Sprinting there now! See you there!
7. Atmosphere: 5
8. Food: 5
9. Service: 5
10. Absolutely heavenly! Perfectly fried, light and fluffy real donuts that just happen to be Vegan!! So many unique flavors and so many textures to choose from. My go-to gift whenever I pass through DC from now on is a pink box of 4 Donut Run donuts!!
11. Atmosphere: 4
12. Food: 5
13. Service: 5
14. Vegan donuts with normal operating hours
15. Atmosphere: 5
16. Food: 5
17. Service: 5
18. Recommended dishes: Doughnut, Glazed Donut, French Toast Donut
19. A few months ago, I went on a donut tour around the DMV looking for the best donuts. I went to all the popular/recommended places and I must say Donut Run is by far the best and its not even close! Not only are the donuts delicious but they have so many different flavors/options to choose from. I have become a regular and have not been disappointed once. 10/10 Highly Recommend!
20. Atmosphere: 5
21. Food: 5
22. Service: 5
23. Recommended dishes: Glazed Donut, French Toast Donut, Raspberry Jelly Filled, Creme Brulee Donut
24. Amazing donuts!!!
25. Atmosphere: 5
26. Food: 5
27. Service: 5
28. The donut was good but pricey.
29. Atmosphere: 3
30. Food: 4
31. Service: 3
32. Probably the most delicious donuts I've ever tried 😍
33. Food: 5
34. Recommended dishes: French Toast Donut
35. Simply the best.
36. I saw a constant stream of people walking by with pink boxes of donuts, so I knew I had to try them. Their pistachio lemon donut was fantastic! Definitely high on the sugar end (I recommend splitting it with someone). Looks like they sell out of donuts, so come early.
37. Atmosphere: 5
"""