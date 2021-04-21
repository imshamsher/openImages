import json
import pandas as pd

json_content = json.load(open("bbox_labels_600_hierarchy.json"))

df = pd.read_csv("oidv6-class-descriptions.csv")

class_name = input("Enter a class_name \t")


siblings = []


parent_dict = None

ancestors_labels = []

found_parent_dict = False
collected_all_ancestors = False

def get_final_subcatogory(j_value, l_name):
    global parent_dict
    global found_parent_dict
    global collected_all_ancestors
    if j_value.get("LabelName",None ) is not None and j_value.get("Subcategory",None ) is not None:
        catgories = j_value["Subcategory"]

        if not found_parent_dict:
            parent_dict = j_value

        for cat in catgories:
            if cat["LabelName"] == l_name :
                found_parent_dict = True
                collected_all_ancestors = True
                return cat
            else:
                if not collected_all_ancestors:
                    ancestors_labels.append(cat["LabelName"])
                get_final_subcatogory(cat,l_name)


def find_hierarchy_parent(j_value, l_name):
    if j_value['LabelName'] == l_name:
        return j_value
    elif 'Subcategory' in j_value:
        for child in j_value['Subcategory']:
            res = find_hierarchy_parent(child, l_name)
            if res is not None:
                return res

    return None

def find_stats(l_name):
    global json_content
    global df
    siblings = []
    final_sub_catogory = get_final_subcatogory(json_content, l_name)
    # print('final subcatagory ', final_sub_catogory)
    # print('parent dict ', parent_dict)

    if final_sub_catogory is not None:
        if final_sub_catogory.get("Subcategory",None) is not None:
            for v in final_sub_catogory["Subcategory"]:
                c_name = df.loc[df['LabelName'] == v["LabelName"], 'DisplayName'].iloc[0]
                siblings.append(c_name)

    print('siblings ', siblings)

    try:
        print('parent_class ',df.loc[df['LabelName'] == parent_dict["LabelName"], 'DisplayName'].iloc[0])
    except :
        print("No parent")

    try:
        ancestors_classes = []
        for l in ancestors_labels:
            ancestors_classes.append(df.loc[df['LabelName'] == l, 'DisplayName'].iloc[0])

        print('ancestors_labels \t', ancestors_labels )

        print('ancestors_classes \t', ancestors_classes )
    except :
        print("No ancestor class")

    pass

try:
    l_name = df.loc[df['DisplayName'] == class_name, 'LabelName'].iloc[0]
    print("labelname ",l_name)
    find_stats(l_name)
except:
    print("No information found")

