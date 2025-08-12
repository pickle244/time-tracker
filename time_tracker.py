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

        self.submit = tk.Button(
            self.root, 
            text='Submit', 
            command=self.fill_csv)

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
        
        self.submit.grid(row=1,column=0)
        
    #     for i, checkbox in enumerate(self.checkboxes):
    #         checkbox.destroy()
    #         self.row_frames[i].destroy()
    #     if (self.submitHours.winfo_exists()):
    #         self.submitHours.grid_forget()

    #     self.checkboxes.clear()
    #     self.checkboxes_checked.clear()
    #     self.entries.clear()
    #     self.row_frames.clear()
    #     self.project_list.clear()

        
    #     for i, project in enumerate(self.project_list):
    #         checked = tk.IntVar()
    #         self.checkboxes_checked.append(checked)

    #         checkbox = tk.Checkbutton(
    #             self.root, 
    #             text=project, 
    #             variable=checked,
    #             command=self.showInputField)
    #         self.checkboxes.append(checkbox)
    #         checkbox.grid(row=i+4, column=0, sticky='w')

    #         row_frame = tk.Frame(self.root)
    #         self.row_frames.append(row_frame)

    #         entry_row = []
    #         for j in range(5):
    #             entry = tk.Entry(row_frame, width = 10)
    #             entry.grid(row=0, column=j)
    #             entry_row.append(entry)

    #         self.entries.append(entry_row)

    #     self.submitHours.grid(row=len(self.project_list)+4, column=0, sticky='w')

    # def showInputField(self):
    #     for i, row_frame in enumerate(self.row_frames):
    #         if (self.checkboxes_checked[i].get()):
    #             row_frame.grid(row=i+4, column=1, sticky='w')
    #         else:
    #             row_frame.grid_forget()

    def fill_csv(self):
        self.out.append(['Projects'] + self.headers[1:] + ['Total'])
        for i, field_row in enumerate(self.fields):
            line = [self.projects[i]]
            total = 0
            for j, field in enumerate(field_row):
                cell = field.get()
                if (j != 4):
                    if (cell == ''):
                        line.append(0.0)
                    else:
                        line.append(float(cell))
                    total += float(cell)
                else:
                    if (cell == ''):
                        line.append('N/A')
                    else:
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