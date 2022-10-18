import tkinter as tk
import time
from pokedex.pokeapi import *


def createWindow(width: int = 800, height: int = 600):
    window = tk.Tk()
    window.geometry(f"{width}x{height}")
    return window


def addSearchBar(root: tk.Tk, async_loop: asyncio.BaseEventLoop):
    global search_field
    search_frame = tk.Frame(master=root)
    search_entry = tk.Entry(master=search_frame)
    search_button = tk.Button(
        master=search_frame,
        text="Search",
        command=lambda s=search_entry, l=async_loop: searchPokemon(s, l),
    )
    search_label = tk.Label(master=search_frame, text="Enter Pokemon name: ")

    search_entry.grid(row=0, column=6, columnspan=5, padx=2, pady=2, sticky="nwse")
    search_button.grid(row=0, column=11, columnspan=2, padx=2, pady=2, sticky="nwse")
    search_label.grid(row=0, column=0, columnspan=5, padx=2, pady=2, sticky="nse")

    for i in range(12):
        search_frame.columnconfigure(i, weight=1, minsize=4)
    search_frame.rowconfigure(0, weight=1)

    search_frame.pack(fill=tk.X)


def searchPokemon(search_field: tk.Entry, async_loop: asyncio.BaseEventLoop):
    param = search_field.get()
    search_field.delete(0, tk.END)
    try:
        results = async_loop.run_until_complete(getPokemon(param))
        stats, details = results
        if len(search_field.winfo_toplevel().winfo_children()) > 1:
            search_field.winfo_toplevel().winfo_children()[1].destroy()
        addPokedexEntry(search_field.winfo_toplevel(), stats, details)
    except Exception as e:
        print(e)
        s = search_field.winfo_toplevel().size()
        error_label = tk.Label(
            master=search_field.winfo_toplevel(),
            text="ERROR INVALID POKEMON NAME",
            fg="red",
        )
        error_label.place(x=0, y=0)


def addPokedexEntry(root: tk.Tk, stats: dict, details: dict):
    print(details["flavor_text_entries"][0]["flavor_text"])
    if len(root.winfo_children()) > 1:
        root.winfo_children()[1].destroy()
    primary_frame = tk.Frame(master=root, bg="blue")

    image_label = tk.Label(
        master=primary_frame,
        text="image",
        bg="red",
    )
    height_label = tk.Label(master=primary_frame, text="height")
    name_label = tk.Label(master=primary_frame, text="name", borderwidth=2)
    category_label = tk.Label(master=primary_frame, text="category", borderwidth=2)
    number_label = tk.Label(master=primary_frame, text="###", borderwidth=2)
    type_label = tk.Label(master=primary_frame, text="types", borderwidth=2)
    abilities_label = tk.Label(master=primary_frame, text="abilities", borderwidth=2)
    weight_label = tk.Label(master=primary_frame, text="weight", borderwidth=2)
    gender_ratio_label = tk.Label(
        master=primary_frame, text="gender ratio", borderwidth=2
    )
    catch_rate_label = tk.Label(master=primary_frame, text="catch rate", borderwidth=2)
    leveling_rate_label = tk.Label(
        master=primary_frame, text="leveling rate", borderwidth=2
    )
    flavor_text_label = tk.Label(
        master=primary_frame, text="flavor text", borderwidth=2
    )
    stats_frame_label = tk.Label(master=primary_frame, text="stats", borderwidth=2)
    breeding_frame_label = tk.Label(
        master=primary_frame, text="breeding", borderwidth=2
    )

    image_label.grid(
        row=0,
        column=0,
        columnspan=4,
        rowspan=4,
        padx=2,
        pady=2,
        sticky="nwse",
    )

    height_label.grid(row=4, column=0, columnspan=4, padx=2, pady=2, sticky="nwse")

    name_label.grid(row=0, column=4, columnspan=3, padx=2, pady=2, sticky="nwse")
    category_label.grid(row=0, column=7, columnspan=3, padx=2, pady=2, sticky="nwse")
    number_label.grid(row=0, column=10, columnspan=2, padx=2, pady=2, sticky="nwse")
    type_label.grid(row=1, column=4, columnspan=8, padx=2, pady=2, sticky="nwse")
    abilities_label.grid(
        row=2, column=4, rowspan=2, columnspan=4, padx=2, pady=2, sticky="nwse"
    )
    weight_label.grid(row=4, column=4, columnspan=4, padx=2, pady=2, sticky="nwse")
    gender_ratio_label.grid(
        row=2, column=8, columnspan=5, padx=2, pady=2, sticky="nwse"
    )
    catch_rate_label.grid(row=3, column=8, columnspan=4, padx=2, pady=2, sticky="nwse")
    leveling_rate_label.grid(
        row=4, column=8, columnspan=4, padx=2, pady=2, sticky="nwse"
    )
    flavor_text_label.grid(
        row=5, column=0, rowspan=2, columnspan=12, padx=2, pady=2, sticky="nwse"
    )
    stats_frame_label.grid(
        row=7, column=0, rowspan=6, columnspan=6, padx=2, pady=2, sticky="nwse"
    )
    breeding_frame_label.grid(
        row=7, column=6, rowspan=6, columnspan=6, padx=2, pady=2, sticky="nwse"
    )

    for i in range(12):
        primary_frame.columnconfigure(i, weight=1, minsize=4)
        primary_frame.rowconfigure(i, weight=1, minsize=2)

    primary_frame.pack(fill=tk.BOTH, expand=True)
