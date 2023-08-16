import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import sqlite3

class SeriesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Series App")
        
        self.series = []
        
        self.series_listbox = tk.Listbox(self)
        self.series_listbox.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.populate_series_list()
        
        self.add_button = tk.Button(self, text="Añadir Serie", command=self.add_series)
        self.add_button.pack(padx=10, pady=5)
        
        self.modify_button = tk.Button(self, text="Modificar Serie", command=self.modify_series)
        self.modify_button.pack(padx=10, pady=5)
        
        self.remove_button = tk.Button(self, text="Eliminar Serie", command=self.remove_series)
        self.remove_button.pack(padx=10, pady=5)
        
        self.connect_to_database()
        
    def populate_series_list(self):
        self.series_listbox.delete(0, tk.END)
        for serie in self.series:
            self.series_listbox.insert(tk.END, f"{serie[1]} - {serie[2]} - Temporada {serie[3]}")
            
    def add_series(self):
        title = simpledialog.askstring("Añadir Serie", "Título de la serie:")
        genre = simpledialog.askstring("Añadir Serie", "Género de la serie:")
        season = simpledialog.askinteger("Añadir Serie", "Temporada de la serie:")
        if title and genre and season:
            self.insert_series(title, genre, season)
            series_id = self.get_last_id()
            self.series.append((series_id, title, genre, season))
            self.populate_series_list()
            
    def modify_series(self):
        selected_index = self.series_listbox.curselection()
        if selected_index:
            series_id = self.series[selected_index[0]][0]
            current_title = self.series[selected_index[0]][1]
            current_genre = self.series[selected_index[0]][2]
            current_season = self.series[selected_index[0]][3]
            new_title = simpledialog.askstring("Modificar Serie", "Nuevo título de la serie:", initialvalue=current_title)
            new_genre = simpledialog.askstring("Modificar Serie", "Nuevo género de la serie:", initialvalue=current_genre)
            new_season = simpledialog.askinteger("Modificar Serie", "Nueva temporada de la serie:", initialvalue=current_season)
            if new_title and new_genre and new_season:
                self.update_series(series_id, new_title, new_genre, new_season)
                self.series[selected_index[0]] = (series_id, new_title, new_genre, new_season)
                self.populate_series_list()
            
    def remove_series(self):
        selected_index = self.series_listbox.curselection()
        if selected_index:
            series_id = self.series[selected_index[0]][0]
            self.delete_series(series_id)
            self.series_listbox.delete(selected_index)
            del self.series[selected_index[0]]
            
    def connect_to_database(self):
        self.connection = sqlite3.connect("series.db")
        self.cursor = self.connection.cursor()
        self.create_series_table()
        self.load_series()
        
    def create_series_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS series (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, genre TEXT, season INTEGER)")
        
    def load_series(self):
        self.cursor.execute("SELECT * FROM series")
        self.series = self.cursor.fetchall()
        self.connection.commit()
        self.populate_series_list()
        
    def insert_series(self, title, genre, season):
        sql = "INSERT INTO series (title, genre, season) VALUES (?, ?, ?)"
        values = (title, genre, season)
        self.cursor.execute(sql, values)
        self.connection.commit()
        
    def update_series(self, series_id, title, genre, season):
        sql = "UPDATE series SET title = ?, genre = ?, season = ? WHERE id = ?"
        values = (title, genre, season, series_id)
        self.cursor.execute(sql, values)
        self.connection.commit()
        
    def delete_series(self, series_id):
        sql = "DELETE FROM series WHERE id = ?"
        values = (series_id,)
        self.cursor.execute(sql, values)
        self.connection.commit()
        
    def get_last_id(self):
        self.cursor.execute("SELECT last_insert_rowid()")
        last_id = self.cursor.fetchone()[0]
        return last_id

if __name__ == "__main__":
    app = SeriesApp()
    app.mainloop()
