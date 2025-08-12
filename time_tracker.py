import csv
import tkinter as tk
import os
from tkinter import messagebox
import datetime

class hourTracker:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title('Hour Tracker')
        self.root.geometry('700x400')

        self.prompt = tk.Label(
            self.root, 
            text='List your projects today, separated by commas:')
        self.prompt.grid(row=0,column=0)

        self.projects = []

        self.response = tk.Entry(self.root,width=50)
        self.response.grid(row=1,column=0)

        self.confirm = tk.Button(
            self.root, 
            text='Confirm', 
            command=self.build_form)
        self.confirm.grid(row=2,column=0)

        self.form = tk.Frame(self.root)

        self.headers = [
            'Track your time:',
            'Coding',
            'Documentation',
            'Testing',
            'Other',
            'Notes']

        self.fields = []

        self.add = tk.Button(self.form,text='+',command=self.add_prompt)

        self.submit = tk.Button(self.root,text='Submit',command=self.fill_csv)

        self.out = []

        self.root.mainloop()

    def build_form(self):
        self.prompt.destroy()
        
        self.projects = [proj.strip() for proj in self.response.get().split(',')]
        self.response.destroy()

        self.confirm.destroy()

        self.form.grid(row=0,column=0)

        for i, header in enumerate(self.headers):
            label = tk.Label(self.form,text=header)
            label.grid(row=0,column=i)
        
        for i, project in enumerate(self.projects):
            label = tk.Label(self.form,text=project)
            label.grid(row=i+1,column=0)

            field_row = []
            for j in range(1,6):
                field = tk.Entry(self.form,width=10)
                field.grid(row=i+1,column=j)
                field_row.append(field)
            self.fields.append(field_row)
        
        self.add.grid(row=len(self.projects)+1,column=0)
        
        self.submit.grid(row=1,column=0)

    def add_prompt(self):
        self.add.grid_forget()

        num_projects = len(self.projects)

        self.enter_proj = tk.Entry(self.form,width=10)
        self.enter_proj.grid(row=num_projects+1,column=0)

        self.confirm = tk.Button(
            self.form,
            text='Confirm',
            command=self.add_form_row)
        self.confirm.grid(row=num_projects+1,column=1)

    def add_form_row(self):
        new_proj = self.enter_proj.get()
        self.projects.append(new_proj)
        num_projects = len(self.projects)

        label = tk.Label(self.form,text=new_proj)
        label.grid(row=num_projects,column=0)

        field_row = []
        for j in range(1,6):
            field = tk.Entry(self.form,width=10)
            field.grid(row=num_projects,column=j)
            field_row.append(field)
        self.fields.append(field_row)

        self.enter_proj.destroy()

        self.confirm.destroy()

        self.add.grid(row=num_projects+1,column=0)

    def fill_csv(self):
        self.out.append(['Projects'] + self.headers[1:] + ['Total'])
        for i, field_row in enumerate(self.fields):
            line = [self.projects[i]]
            total = 0
            for j, field in enumerate(field_row):
                cell = field.get()
                if (j != 4):
                    if (cell == ''):
                        cell = 0
                    line.append(float(cell))
                    total += float(cell)
                else:
                    if (cell == ''):
                        cell = 'n/a'
                    line.append(cell)

                field.delete(0, tk.END)
            line.append(total)
            self.out.append(line)

        filePath = os.path.abspath(__file__)
        dirPath = os.path.join(os.path.dirname(filePath), 'time_tracker.csv')
        try:
            with open(dirPath, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                date = datetime.datetime.now().strftime('%A, %B %d, %Y')
                writer.writerow([date])
                for line in self.out:
                    writer.writerow(line)
                csvfile.close()
                self.root.destroy()
        except:
            messagebox.showwarning('Warning', 'Error writing to file')
            self.out.clear()

hourTracker()