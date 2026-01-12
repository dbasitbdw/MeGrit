from datetime import datetime, date, timedelta
import json
import os

class TaskManager:
    
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tasks.json')
        self.tasks = []
        self.next_id = 1
        self.current_user = None
        self.load_tasks()

    def set_user(self, username):
        self.current_user = username

    def _get_user_tasks(self):
        if not self.current_user:
            return []
        return [t for t in self.tasks if t.get('username') == self.current_user]
    
    def add_task(self, task_data):
        task = {
            'id': self.next_id,
            'description': task_data.get('description', ''),
            'category': task_data.get('category', 'Other'),
            'priority': task_data.get('priority', 'Low'),
            'status': task_data.get('status', 'Pending'),
            'username': self.current_user, # Associate with current user
            # Allow overriding created_at directly or via scheduled info
            'created_at': task_data.get('created_at') or self._parse_date(task_data) or datetime.now(),
            'updated_at': datetime.now(),
            'scheduled_date': task_data.get('scheduled_date'),
            'scheduled_time': task_data.get('scheduled_time')
        }
        
        print(f"DEBUG: Adding task for user {self.current_user}: {task['created_at']}")
        
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        
        return task

    def _parse_date(self, task_data):
        if 'scheduled_date' in task_data and 'scheduled_time' in task_data:
            try:
                # Format: dd/MM/yy HH.mm
                dt_str = f"{task_data['scheduled_date']} {task_data['scheduled_time']}"
                print(f"DEBUG: Parsing date string: {dt_str}")
                parsed = datetime.strptime(dt_str, "%d/%m/%y %H.%M")
                print(f"DEBUG: Parsed successfully: {parsed}")
                return parsed
            except Exception as e:
                print(f"DEBUG: Date parsing failed for '{dt_str}': {e}")
        return None
    
    def update_task(self, task_id, task_data):
        for task in self.tasks:
            if task['id'] == task_id:
                task.update(task_data)
                task['updated_at'] = datetime.now()
                self.save_tasks()
                return task
        
        return None
    
    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        
        return False
    
    def get_all_tasks(self):
        return self._get_user_tasks()
    
    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        
        return None
    
    def count_today_entries(self):
        today = date.today()
        count = 0
        
        for task in self._get_user_tasks():
            if hasattr(task['created_at'], 'date'):
                 if task['created_at'].date() == today:
                    count += 1
        
        return count
    
    def count_completed_tasks(self):

        user_tasks = self._get_user_tasks()
        return sum(1 for task in user_tasks if task.get('status') == 'Completed')
    
    def get_completion_percentage(self):
        user_tasks = self._get_user_tasks()
        if not user_tasks:
            return 0.0
        
        completed = self.count_completed_tasks()
        return (completed / len(user_tasks)) * 100

    def load_tasks(self):
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, 'r') as f:
                content = f.read()
                if not content:
                    return
                    
                data = json.loads(content)
                self.tasks = []
                max_id = 0
                
                for item in data:
                    if 'created_at' in item:
                        item['created_at'] = datetime.fromisoformat(item['created_at'])
                    if 'updated_at' in item:
                        item['updated_at'] = datetime.fromisoformat(item['updated_at'])
                    
                    self.tasks.append(item)
                    max_id = max(max_id, item.get('id', 0))
                
                self.next_id = max_id + 1
                
        except json.JSONDecodeError:
            print(f"Error decoding {self.data_file}")
            self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:

            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

            data_to_save = []
            for task in self.tasks:
                task_copy = task.copy()
                if isinstance(task_copy.get('created_at'), (datetime, date)):
                    task_copy['created_at'] = task_copy['created_at'].isoformat()
                if isinstance(task_copy.get('updated_at'), (datetime, date)):
                    task_copy['updated_at'] = task_copy['updated_at'].isoformat()
                data_to_save.append(task_copy)
            
            with open(self.data_file, 'w') as f:
                json.dump(data_to_save, f, indent=4)
                
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def calculate_streak(self):
        today = date.today()
        streak_count = 0

        completed_dates = set()
        for task in self._get_user_tasks():
            if task.get('status') == 'Completed':
      
                d = None
                if 'scheduled_date' in task and 'scheduled_time' in task:
                     try:
                        dt_str = f"{task['scheduled_date']} {task['scheduled_time']}"
                        d = datetime.strptime(dt_str, "%d/%m/%y %H.%M").date()
                     except:
                        pass
                
                if not d:
                    created_at = task.get('created_at')
                    if isinstance(created_at, datetime):
                        d = created_at.date()
                    elif isinstance(created_at, str):
                        try:
                            d = datetime.fromisoformat(created_at).date()
                        except:
                            pass
                
                if d:
                    completed_dates.add(d)
        
        if not completed_dates:
            return 0
            
        sorted_dates = sorted(list(completed_dates))
 
        max_streak = 0
        current_streak = 0
        
        for i in range(len(sorted_dates)):
            if i == 0:
                current_streak = 1
            else:
                diff = (sorted_dates[i] - sorted_dates[i-1]).days
                if diff == 1:
                     current_streak += 1
                elif diff == 0:
                    pass 
                else:
                    current_streak = 1
            max_streak = max(max_streak, current_streak)
            
        return min(max_streak, 7)

    def _has_activity_on_date(self, check_date):
        for task in self._get_user_tasks():
            if isinstance(task.get('created_at'), datetime):
                if task['created_at'].date() == check_date:
                    return True
            elif isinstance(task.get('created_at'), str):
                try:
                    task_date = datetime.fromisoformat(task['created_at']).date()
                    if task_date == check_date:
                        return True
                except:
                    pass
        return False

    def update_task_status(self, task_id, is_completed):
        status = "Completed" if is_completed else "Pending"
        self.update_task(task_id, {'status': status})
