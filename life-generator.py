import sys, csv
import pandas as pd
from tkinter import *
from tkinter import ttk
from pandastable import Table

def findTopToys(datasource, quantity, category, frame):
  quantity = int(float(quantity))
  data = pd.read_csv(datasource, delimiter=',')
  data = data.loc[data['amazon_category_and_sub_category'].str.contains(category, na=False)]
  sorted_data = data.sort_values(['uniq_id', 'number_of_reviews'], ascending=[True, False])[0:quantity*10]
  result = sorted_data.sort_values(['uniq_id', 'average_review_rating'], ascending=[True, False])[0:quantity]

  pt = Table(frame, dataframe=result)
  pt.show()
  pt.redraw()

  return result

def getCategories(datasource):
  with open(datasource) as source:
    reader = csv.DictReader(source)
    data = {}
    for row in reader:
      for header, value in row.items():
        try:
          data[header].append(value)
        except KeyError:
          data[header] = [value]
    
    categories = data['amazon_category_and_sub_category']
    stripped_categories = [] * len(categories)
    for category in categories:
      stripped_categories.append(category.split('>')[0].strip())
    
    unique_categories = list(set(stripped_categories))
    return list(filter(None, unique_categories))

def getVariables(source):
  with open(source) as source:
    reader = csv.DictReader(source)
    data = {}
    for row in reader:
      for header, value in row.items():
        try:
          data[header].append(value)
        except KeyError:
          data[header] = [value]
    
    return data['input_item_category'], data['input_number_to_generate']

def exportToCsv(top_toys, category, quantity):
  quantity = int(float(quantity))
  header = ['input_item_type', 'input_item_category', 'input_number_to_generate', 'output_item_name', 'output_item_rating', 'output_item_num_reviews']

  with open('output.csv', mode='w') as output:
    output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(header)
    top_toys['input_item_type'] = 'toys'

    if type(category) == list:
      top_toys['input_item_category'] = category[0]
    else:
      top_toys['input_item_category'] = category

    if type(category) == list:
      top_toys['input_number_to_generate'] = quantity[0]
    else:
      top_toys['input_number_to_generate'] = quantity
    
    top_toys.to_csv(output, columns=['input_item_type', 'input_item_category', 'input_number_to_generate','product_name', 'average_review_rating', 'number_of_reviews'], header=False, index=False)

def main():
  datasource = "datasource.csv"
  input_item_type = "toys"
  categories = getCategories(datasource)
  
  if len(sys.argv) > 1:
    input_variables = sys.argv[1]
    input_item_category, input_number_to_generate = getVariables(sys.argv[1])
    top_toys = findTopToys(datasource, int(input_number_to_generate[0]), input_item_category[0])
    exportToCsv(top_toys, input_item_category, input_number_to_generate)


  root = Tk()
  root.title("Life Generator")
  root.geometry("500x500")

  Label(root, text="Choose a category").pack()
  input_item_category = StringVar(root)
  category_input = OptionMenu(root, input_item_category, *categories).pack()


  Label(root, text="Number to generate").pack()
  quantity = StringVar(root)
  quantity_input = Entry(root, textvariable=quantity)
  quantity_input.pack()

  frame = Frame(root)
  frame.pack(fill='both', expand=True)
  
  generate_results = Button(root, text="Generate Results", command=lambda : findTopToys(datasource, quantity_input.get(), input_item_category.get(), frame)).pack()
  generate_csv = Button(root, text="Generate CSV", command=lambda : exportToCsv(findTopToys(datasource, quantity_input.get(), input_item_category.get(), frame), input_item_category.get(), quantity_input.get())).pack()

  mainloop()

if __name__ == '__main__':
  main()