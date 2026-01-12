class CategoryManager:
  
    DEFAULT_CATEGORIES = ["Work", "Personal", "Study", "Health", "Other"]
    
    @staticmethod
    def get_categories():

        return CategoryManager.DEFAULT_CATEGORIES
    
    @staticmethod
    def count_by_category(tasks):
        counts = {category: 0 for category in CategoryManager.DEFAULT_CATEGORIES}
        
        for task in tasks:
            category = task.get('category', 'Other')
            if category in counts:
                counts[category] += 1
            else:
                counts['Other'] += 1
        
        return counts
    
    @staticmethod
    def get_category_color(category):
        colors = {
            "Work": "#9AB3D5",
            "Personal": "#e8a8a6",
            "Study": "#f7f2b3",
            "Health": "#b3d5b3",
            "Other": "#d5d5d5"
        }
        return colors.get(category, "#d5d5d5")
