# Functional; scrape text from pdf using a url
import requests
import io
from pdfminer.high_level import extract_text

def scrape_tatte_menu(pdf_url):
    """
    Scrapes the Tatte Bakery menu from a PDF URL and returns it as a string.

    Args:
        pdf_url (str): The URL of the PDF menu.

    Returns:
        str: The extracted text from the PDF, or None if an error occurred.
    """
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        pdf_file = io.BytesIO(response.content)
        text = extract_text(pdf_file)
        return text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching PDF: {e}")
        return None
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

if __name__ == "__main__":
    pdf_url = "https://tattebakery.com/wp-content/uploads/2024/10/Fall2024_AllDay_101524.pdf"
    menu_text = scrape_tatte_menu(pdf_url)

    if menu_text:
        print(menu_text)
    else:
        print("Failed to retrieve the menu.")

""" IT WORKED. Again, thanks to Perplexity. 
Example output:

A L L   D A Y   M E N U

B r e a k f a s t

B R E A K F A S T   S A N D W I C H * 
Eggs your style*, VT cheddar, and applewood smoked 
bacon, on housemade sourdough. 870 cal. wmeG

S AU S A G E   B R E A K FA S T   S A N DW I C H * 
Housemade Sujuk-spiced beef sausage with an  
egg your style*, VT cheddar, & tomato on a   
housemade challah roll. 810 cal. wmeG

C R O I S S A N T   B R E A K F A S T   
S A N D W I C H * 
Egg your style*, VT cheddar, sliced tomato, avocado,  
& baby arugula on a housemade croissant. 680 cal. 
wmeGv  Add housemade beef sausage (160 cal). 

H A L L O U M I   S U N N Y- S I D E 
B R E A K F A S T   S A N D W I C H * 
Seared halloumi cheese, griddled tomato, sautéed spinach 
with a sunny-side up egg*, on a challah roll. 520 cal. 

wmegv Add housemade beef sausage (160 cal).

S M O K E D   S A L M O N ,   A V O C A D O ,                  

&   E G G   S A N D W I C H * 
Smoked salmon*, avocado, red onion, capers, alfalfa sprouts, 
& creamy scrambled eggs, served on a housemade challah 
roll, with a green herb dressing. 630 cal. wmefsG        

E G G   I N   A   H O L E * 
Two fried eggs* nestled in a housemade sesame Jerusalem 
bagel. Served with chopped vegetable salad. 680 cal. 

wmezv Add ham & VT cheddar (180 cal).

L A M B   H A S H * 
Lamb cooked in warm spices sautéed with potatoes, 
sweet potatoes, carrots, and pickled red cabbage, topped 
with a poached egg* and green dressing, with roasted 
garlic labneh and tomato salad. 760 cal. Served with 
housemade challah, 170 cal. wmesG

C R O Q U E   M A D A M E * 
Housemade croissant, ham, Gruyère, & an egg your 
style*. Topped with Mornay sauce. 790 cal. wme

H O U S E   B R E A K F A S T   P L A T E * 
Two eggs your style*, applewood smoked bacon, and 
potato fritters with tomato jam & mint parmesan. 
470 cal. Served with housemade sourdough, 190 cal. 
wmeG Add housemade beef sausage (160 cal).
"""