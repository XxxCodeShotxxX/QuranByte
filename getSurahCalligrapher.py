from bs4 import BeautifulSoup
import os,  requests
from PIL import Image,ImageOps

from svg2png import svg2png





def getSurahCalligrapherSvg():

    url = "https://quranonline.net/the-holy-quran/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("img", {"src": lambda x:x.endswith(".svg")})

    output_directory = "C:/Users/A M ! N E/Desktop/QuranByte/images/calligrapher/"
    for link in links:
        link = link['src']
        filename = link.split('/')[-1]
        print(filename)
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(requests.get(link).content)
            print(f"Downloaded: {filename}")

    

    
def svgToPng():
    svg_directory = "C:\\Users\\A M ! N E\\Desktop\\QuranByte\\images\\calligrapher\\svg\\"
    output_directory = "C:\\Users\\A M ! N E\\Desktop\\QuranByte\\images\\calligrapher\\png\\"
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(svg_directory):
        if filename.endswith(".svg"):
            input_file = os.path.join(svg_directory, filename)
            print("input_file: ",input_file)
            output_file = os.path.join(output_directory, filename[:-3] + "png")
            print("output_file: ",output_file)
            with open(input_file, 'rb') as svg_file:
                png = svg2png(input_file)
                with open(output_file, 'wb') as png_file:
                    png_file.write(png)
            print(f"Converted {input_file} to {output_file}")




def removeBackground():
    png_directory = "C:\\Users\\A M ! N E\\Desktop\\QuranByte\\images\\calligrapher\\png\\"
    output_directory = "C:\\Users\\A M ! N E\\Desktop\\QuranByte\\images\\calligrapher\\png\\"

    for filename in os.listdir(png_directory):
        if filename.endswith('.png'):
            png_path = os.path.join(png_directory, filename)
            png_no_bg_path = os.path.join(output_directory, filename)
            
            png_image = Image.open(png_path)
            png_image = png_image.convert("RGBA")
            datas = png_image.getdata()
            
            # Create new pixel data with transparent background
            new_data = []
            for item in datas:
                # Keep white pixels (adjust tolerance as needed)
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    new_data.append(item)
                else:
                    new_data.append((255, 255, 255, 0))  # Make non-white pixels transparent
            
            # Update image with new pixel data
            png_image.putdata(new_data)
            
            # Save image with transparent background
            png_image.save(png_no_bg_path, "PNG")
            
            print(f"Processed: {filename}")    




def invert_image(ayah_image):
    image = Image.open(f"images/ayah png/{ayah_image}").convert('RGBA')
    r, g, b, a = image.split()
    r, g, b = map(ImageOps.invert, (r, g, b))
    inverted_image = Image.merge(image.mode, (r, g, b, a))
    inverted_image.save(f"images/ayah png/{ayah_image}", 'PNG')



def invert_ayat():
    for ayah in os.listdir("images/ayah png"):
        invert_image(ayah)
