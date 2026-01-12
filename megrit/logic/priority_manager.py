class PriorityManager:
    
    # Priority levels
    PRIORITY_LEVELS = ["Low", "Medium", "High"]
    
    @staticmethod
    def get_priorities():
  
        return PriorityManager.PRIORITY_LEVELS
    
    @staticmethod
    def count_high_priority(tasks):
 
        return sum(1 for task in tasks if task.get('priority', '') == 'High' and task.get('status') != 'Completed')
    
    @staticmethod
    def count_by_priority(tasks):
  
        counts = {priority: 0 for priority in PriorityManager.PRIORITY_LEVELS}
        
        for task in tasks:
            priority = task.get('priority', 'Low')
            if priority in counts:
                counts[priority] += 1
        
        return counts
    
    @staticmethod
    def get_priority_color(priority):
  
        colors = {
            "Low": "#b3d5b3",
            "Medium": "#f7f2b3",
            "High": "#e8a8a6"
        }
        return colors.get(priority, "#d5d5d5")
    
    @staticmethod
    def get_priority_weight(priority):

        weights = {
            "High": 3,
            "Medium": 2,
            "Low": 1
        }
        return weights.get(priority, 0)
