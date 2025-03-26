output_dict = [['Butter Chicken: No description', 'Butter Chicken'], ['Vegetable Biryani: No description', 'Biryani'], ['Chicken Biryani: No description', 'Biryani'], ['Goat Biryani (Hyderabadi Style): No description', 'Biryani'], ['Samosa Chaat: Well -cooked samosa tossed with yogurt, onion, tamarind sauce and chickpeas', 'Samosas'], ['Vegetable Samosa (2 PC): Triangular pastries filled with potatoes and peas with a touch of spices', 'Samosas'], ['Mixed Platter: 2 pcs samosa, 2 pcs alu tikki, 4 pcs vegetable pakora', 'Samosas']]

#print each item in the output_dict but only before the colon
for item in output_dict:
    print(item[0].split(':')[0])
