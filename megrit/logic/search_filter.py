class SearchFilter:
    
    @staticmethod
    def filter_by_description(tasks, query):
 
        if not query:
            return tasks
        
        query = query.lower()
        return [task for task in tasks if query in task.get('description', '').lower()]
    
    @staticmethod
    def filter_by_category(tasks, category):

        if not category or category == "All":
            return tasks
        
        return [task for task in tasks if task.get('category', '') == category]
    
    @staticmethod
    def filter_by_priority(tasks, priority):
   
        if not priority or priority == "All":
            return tasks
        
        return [task for task in tasks if task.get('priority', '') == priority]
    
    @staticmethod
    def filter_by_status(tasks, status):
  
        if not status or status == "All":
            return tasks
        
        return [task for task in tasks if task.get('status', '') == status]
    
    @staticmethod
    def combined_filter(tasks, description=None, category=None, priority=None, status=None):

        filtered = tasks
        
        if description:
            filtered = SearchFilter.filter_by_description(filtered, description)
        if category:
            filtered = SearchFilter.filter_by_category(filtered, category)
        if priority:
            filtered = SearchFilter.filter_by_priority(filtered, priority)
        if status:
            filtered = SearchFilter.filter_by_status(filtered, status)
        
        return filtered
