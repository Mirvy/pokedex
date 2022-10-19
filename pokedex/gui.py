import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from pokedex.pokeapi import *


def createWindow(width: int = 800, height: int = 600):
    window = tk.Tk()
    window.geometry(f"{width}x{height}")
    return window


def addSearchBar(root: tk.Tk, async_loop: asyncio.BaseEventLoop):
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
    global IMAGE
    param = search_field.get()
    search_field.delete(0, tk.END)
    try:
        results = async_loop.run_until_complete(getPokemon(param))
        stats, details, image = results
        print(image)
        im = BytesIO(image)
        im = Image.open(im)
        im = im.resize((410, 320))
        IMAGE = ImageTk.PhotoImage(im)
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
    global IMAGE
    print(details["flavor_text_entries"][0]["flavor_text"])
    if len(root.winfo_children()) > 1:
        root.winfo_children()[1].destroy()
    primary_frame = tk.Frame(master=root, bg="blue")
    image_canvas = tk.Canvas(master=primary_frame, relief=tk.RIDGE, borderwidth=3)
    image_canvas.create_image(0, 0, image=IMAGE, anchor=tk.NW)
    height_label = tk.Label(
        master=primary_frame, text="height", relief=tk.RIDGE, borderwidth=3, bg="white"
    )
    name_label = tk.Label(
        master=primary_frame,
        text=stats["name"].capitalize(),
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    category = ""
    for g in details["genera"]:
        if g["language"]["name"] == "en":
            category = g["genus"]
            break
    category_label = tk.Label(
        master=primary_frame,
        text=category,
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    number_label = tk.Label(
        master=primary_frame,
        text=stats["order"],
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    types = ""
    for t in stats["types"]:
        types += t["type"]["name"] + " "
    type_label = tk.Label(
        master=primary_frame, text=types, relief=tk.RIDGE, borderwidth=3, bg="white"
    )
    abilities_label = tk.Label(
        master=primary_frame,
        text="abilities",
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    weight_label = tk.Label(
        master=primary_frame, text="weight", relief=tk.RIDGE, borderwidth=3, bg="white"
    )
    gender_ratio_label = tk.Label(
        master=primary_frame,
        text="gender ratio",
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    catch_rate_label = tk.Label(
        master=primary_frame,
        text="catch rate",
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    leveling_rate_label = tk.Label(
        master=primary_frame,
        text="leveling rate",
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    flavor_text = ""
    for ft in details["flavor_text_entries"]:
        if ft["language"]["name"] == "en":
            flavor_text = ft["flavor_text"]
            break
    flavor_text = flavor_text.replace("\n", " ")
    flavor_text_label = tk.Label(
        master=primary_frame,
        text=flavor_text,
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )
    stats_frame_label = tk.Label(
        master=primary_frame, text="stats", relief=tk.RIDGE, borderwidth=3, bg="white"
    )
    breeding_frame_label = tk.Label(
        master=primary_frame,
        text="breeding",
        relief=tk.RIDGE,
        borderwidth=3,
        bg="white",
    )

    image_canvas.grid(
        row=0,
        column=0,
        columnspan=4,
        rowspan=4,
        sticky="nwse",
    )

    height_label.grid(row=4, column=0, columnspan=4, sticky="nwse")

    name_label.grid(row=0, column=4, columnspan=3, sticky="nwse")
    category_label.grid(row=0, column=7, columnspan=3, sticky="nwse")
    number_label.grid(row=0, column=10, columnspan=2, sticky="nwse")
    type_label.grid(row=1, column=4, columnspan=8, sticky="nwse")
    abilities_label.grid(row=2, column=4, rowspan=2, columnspan=4, sticky="nwse")
    weight_label.grid(row=4, column=4, columnspan=4, sticky="nwse")
    gender_ratio_label.grid(row=2, column=8, columnspan=5, sticky="nwse")
    catch_rate_label.grid(row=3, column=8, columnspan=4, sticky="nwse")
    leveling_rate_label.grid(row=4, column=8, columnspan=4, sticky="nwse")
    flavor_text_label.grid(row=5, column=0, rowspan=2, columnspan=12, sticky="nwse")
    stats_frame_label.grid(row=7, column=0, rowspan=6, columnspan=6, sticky="nwse")
    breeding_frame_label.grid(row=7, column=6, rowspan=6, columnspan=6, sticky="nwse")

    for i in range(12):
        primary_frame.columnconfigure(i, weight=i, minsize=2)
        primary_frame.rowconfigure(i, weight=i, minsize=2)

    primary_frame.pack(fill=tk.BOTH, expand=True)
