import sys, csv
import pandas as pd
from tkinter import *
from tkinter import ttk
from pandastable import Table

def findTopToys(datasource, quantity, category, frame):
  quantity = int(float(quantity))
  data = pd.read_csv(datasource, delimiter=',')
  data = data.loc[data['amazon_category_and_sub_category'].str.contains(category, na=False)]
  sorted_data = data.sort_values(
    ['uniq_id', 'number_of_reviews'], ascending=[True, False])[0:quantity*10]
  result = sorted_data.sort_values(
    ['uniq_id', 'average_review_rating'], ascending=[True, False])[0:quantity]

  renderTable(frame, result)
  return result

def renderTable(frame, data):
  pt = Table(frame, dataframe=data)
  pt.show()
  pt.redraw()

def readCsv(datasource):
  data = {}
  with open(datasource) as source:
    reader = csv.DictReader(source)
    for row in reader:
      for header, value in row.items():
        try:
          data[header].append(value)
        except KeyError:
          data[header] = [value]

  return data

def getCategories(datasource):
  data = readCsv(datasource)
    
  stripped_categories = []
  for category in data['amazon_category_and_sub_category']:
    stripped_categories.append(category.split('>')[0].strip())
  
  unique_categories = list(set(stripped_categories))
  return list(filter(None, unique_categories))

def getVariables(datasource):
  data = readCsv(datasource)  
  return data['input_item_category'], data['input_number_to_generate']

def exportToCsv(top_toys, category, quantity):
  header = [
    'input_item_type', 'input_item_category', 'input_number_to_generate', 
    'output_item_name', 'output_item_rating', 'output_item_num_reviews']

  with open('output.csv', mode='w') as output:
    output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(header)
    top_toys['input_item_type'] = 'toys'

    if type(category) == list:
      top_toys['input_item_category'] = category[0]
      top_toys['input_number_to_generate'] = quantity[0]
    else:
      top_toys['input_item_category'] = category
      top_toys['input_number_to_generate'] = int(float(quantity))
    
    top_toys.to_csv(
      output, 
      columns=['input_item_type', 'input_item_category', 'input_number_to_generate',
      'product_name', 'average_review_rating', 'number_of_reviews'], header=False, index=False)

def buildGui(root, categories, datasource, frame):
  Label(root, text="Choose a category").pack()
  input_item_category = StringVar(root)
  category_input = OptionMenu(root, input_item_category, *categories).pack()

  Label(root, text="Number to generate").pack()
  quantity = StringVar(root)
  quantity_input = Entry(root, textvariable=quantity)
  quantity_input.pack()

  generate_results = Button(
    root, text="Generate Results", 
    command=lambda : findTopToys(datasource, quantity_input.get(), input_item_category.get(), frame)
    ).pack()

  generate_csv = Button(
    root, text="Generate CSV", 
    command=lambda : exportToCsv(findTopToys(datasource, quantity_input.get(), 
    input_item_category.get(), frame), input_item_category.get(), quantity_input.get())
    ).pack()
  
def main():
  datasource = "datasource.csv"
  input_item_type = "toys"
  categories = getCategories(datasource)
  
  root = Tk()
  root.title("Life Generator")
  root.geometry("500x500")
  frame = Frame(root)
  frame.pack(fill='both', expand=True)
  buildGui(root, categories, datasource, frame)

  if len(sys.argv) > 1:
    input_item_category, input_number_to_generate = getVariables(sys.argv[1])
    top_toys = findTopToys(
      datasource, int(input_number_to_generate[0]), input_item_category[0], frame)
    exportToCsv(top_toys, input_item_category, input_number_to_generate)
  
  mainloop()

if __name__ == '__main__':
  main()