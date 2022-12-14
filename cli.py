
from typing import Optional

from habittracker import __app_name__, __version__, database, model, get, analytics

import questionary

import datetime

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()

console = Console()

qt = questionary


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=version_callback,
        is_eager=True
    )
) -> None:
    return



habit_name = get.habit_entry
description_name = get.habit_description
periodicity_name = get.habit_periodicity
operating_habit = get.habits_of_database
get_periodicity_name = get.analyze_habit_periodicity
periodicity_change_name = get.habit_periodicity_change





@app.command(short_help="Start your very own habittracker")
def start():
    db = database.connect_db()
    if len(database.all_habits(db)) == 0:
        typer.secho("\nWELCOME !!! TIME TO WORK ON YOUR HABITS !!!",fg=typer.colors.BRIGHT_GREEN)
        typer.secho("\nRight now your habittracker is empty,\n", fg=typer.colors.BRIGHT_RED)
        start_question = qt.confirm("Do you want to start your app and add a habit to your tracker ?").ask()
        if start_question:
            start_continuing_question = qt.select("What do you want to do?",
            choices=["Editting", "Managing", "Analyzing", "Exit"],
            ).ask()
            if start_continuing_question == "Editting":
                edit()
            elif start_continuing_question == "Managing":
                manage()
            elif start_continuing_question == "Analyzing":
                analyze()
            else:
                typer.secho("\nYou're leaving your app at this moment ! Besides the 'start' command,\n\nyou can directly insert a habit with the 'edit' command ! Otherwise:",
                fg=typer.colors.BRIGHT_YELLOW)
                typer.secho("\nType 'python -m habittracker --help' to see your command options for this app !\n",
                fg=typer.colors.BRIGHT_YELLOW)
                exit_start_is_on = True
                while exit_start_is_on:
                    exit_start_question = qt.confirm("Are you sure you want to exit ?").ask()
                    if exit_start_question:
                        typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                        fg=typer.colors.BRIGHT_CYAN)
                        exit_start_is_on = False
                        raise typer.Exit()
                    else:
                        counter_exit_start_question = qt.select("What do you want to do?",
                        choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                        ).ask()
                        if counter_exit_start_question == "Editting":
                            edit()
                        elif counter_exit_start_question == "Managing":
                            manage()
                        elif counter_exit_start_question == "Analyzing":
                            analyze()
                        elif counter_exit_start_question == "Go to Start":
                            start()
                        else:
                            exit_start_question

    elif len(database.all_habits(db)) > 0:
        show(None)
        typer.secho("\nWELCOME !!! TIME TO WORK ON YOUR HABITS !!!\n",fg=typer.colors.BRIGHT_GREEN)
        second_start_quesiton = qt.select("What do you want to do ?",
        choices=["Editting", "Managing", "Analyzing", "Exit"]
        ).ask()
        if second_start_quesiton == "Editting":
            edit()
        elif second_start_quesiton == "Managing":
            manage()
        elif second_start_quesiton == "Analyzing":
            analyze()
        else:
            exit_start_show_is_on = True
            while exit_start_show_is_on:
                exit_start_show_question = qt.confirm("Are you sure you want to exit ?").ask()
                if exit_start_show_question:
                        typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                        fg=typer.colors.BRIGHT_CYAN)
                        exit_start_show_is_on = False
                        raise typer.Exit()
                else:
                    counter_exit_start_show_question = qt.select("What do you want to do?",
                    choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                        ).ask()
                    if counter_exit_start_show_question == "Editting":
                        edit()
                    elif counter_exit_start_show_question == "Managing":
                        manage()
                    elif counter_exit_start_show_question == "Analyzing":
                        analyze()
                    elif counter_exit_start_show_question == "Go to Start":
                        start()
                    else:
                        exit_start_show_question
    

@app.command()
def log():
    db = database.connect_db()
    if len(database.all_log(db)) != 0:
        log_data = database.all_log(db)
        table = Table(title = "\nHABITLOG\n", show_header=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Completed", min_width=12, justify="center")
        table.add_column("Streak", min_width=12, justify="center")
        table.add_column("Completed_Time", min_width=12, justify="center")
            
        for infos in log_data:
            is_completed_str = 'Yes' if infos.completed == 2 else 'No'
            table.add_row( infos.habit, is_completed_str, str(infos.streak), infos.datetime_completed)
        console.print(table)
    
    else:
        typer.secho("\nThere is no data in your habitlog !\n",
        fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()
    


@app.command(short_help="See an overview of your habits in a table")
def show(periodicity: Optional[str] = typer.Argument(None)):
    try:
        if periodicity is None:
            db = database.connect_db()
            if len(database.all_habits(db)) > 0:
                entries_list = database.all_habits(db)
                table = Table(title="\nYOUR HABITTRACKER\n", show_header=True, show_lines=True)
                table.add_column("Habit", min_width=12, justify="center")
                table.add_column("Description", min_width=20, justify="center")
                table.add_column("Periodicity", min_width=12, justify="center")
                table.add_column("Start", min_width=12, justify="center")
                table.add_column("Completed", min_width=12, justify="center")
                table.add_column("Streak", min_width=12, justify="center")

                for entry in entries_list:
                    is_completed_str = 'Yes' if entry.completed == 2 else 'No'
                    table.add_row(entry.habit, entry.description, entry.periodicity, entry.starting_date, is_completed_str, str(entry.streak))
                console.print(table)
            else:
                typer.secho(f"\nThere are no habits in your database ! Please add one first !\n", fg=typer.colors.BRIGHT_RED)
                adding_question = qt.confirm("Do you want to add a habit?").ask()
                if adding_question:
                    edit()

        elif periodicity == "Daily":
            db = database.connect_db()
            if len(database.all_habits(db)) > 0:
                data_list = analytics.habit_custom_perdiodicity_information(db,periodicity)
                table = Table(title="\nYOUR HABITTRACKER\n", show_header=True, show_lines=True)
                table.add_column("Habit", min_width=12, justify="center")
                table.add_column("Description", min_width=20, justify="center")
                table.add_column("Periodicity", min_width=12, justify="center")
                table.add_column("Start", min_width=12, justify="center")
                table.add_column("Completed", min_width=12, justify="center")
                table.add_column("Streak", min_width=12, justify="center")

                for data in data_list:
                    completed_daily_str = 'Yes' if data.completed == 2 else 'No'
                    table.add_row(data.habit, data.description, data.periodicity, data.starting_date, completed_daily_str, str(data.streak))
                console.print(table)

            else:
                typer.secho(f"\nThere are no habits in your database ! Please add one first !\n", fg=typer.colors.BRIGHT_RED)
                raise typer.Abort()

        elif periodicity == "Weekly":
            db = database.connect_db()
            if len(database.all_habits(db)) > 0:
                periodicity_list = analytics.habit_custom_perdiodicity_information(db,periodicity)
                table = Table(title="\nYOUR HABITTRACKER\n", show_header=True, show_lines=True)
                table.add_column("Habit", min_width=12, justify="center")
                table.add_column("Description", min_width=20, justify="center")
                table.add_column("Periodicity", min_width=12, justify="center")
                table.add_column("Start", min_width=12, justify="center")
                table.add_column("Completed", min_width=12, justify="center")
                table.add_column("Streak", min_width=12, justify="center")

                for period in periodicity_list:
                    completed_weekly_str = 'Yes' if period.completed == 2 else 'No'
                    table.add_row(period.habit, period.description, period.periodicity, period.starting_date, completed_weekly_str, str(period.streak))
                console.print(table)

            else:
                typer.secho(f"\nThere are no habits in your database ! Please add one first !\n", fg=typer.colors.BRIGHT_RED)
                raise typer.Abort()
            
    except TypeError:
        typer.secho("\nThere are no habits in your table !! Please add a habit!\n", fg=typer.colors.BRIGHT_RED)
        raise typer.Abort()



@app.command(short_help="Add or Delete a habit")
def edit():
    edit_question = qt.select("What do you want to edit?",
    choices=["Add", "Delete", "Go to Start", "Exit"],
    ).ask()

    if edit_question == "Add":
        adding_is_on = True
        db = database.connect_db()
        while adding_is_on:
            try:
                habit_entry = habit_name()
                if database.habit_existing_check(db, habit_entry) is False:
                    description_entry = description_name()
                    periodicity_entry = periodicity_name()
                    adding_entry = model.Habit(habit_entry, description_entry, periodicity_entry)
                    if get.adding_confirmation(habit_entry, description_entry, periodicity_entry):
                        model.Habit.add_habit(adding_entry)
                        show(None)
                        typer.secho(f"\nYou added the habit '{habit_entry}' with the description '{description_entry}' as '{periodicity_entry}' to your tracker!!\n",
                        fg=typer.colors.BRIGHT_GREEN)
                    else:
                        typer.secho(f"\nThe habit '{habit_entry}' was NOT added to your tracker! Please try again!\n", fg=typer.colors.BRIGHT_RED)
                else:
                    typer.secho(f"\nThe habit '{habit_entry}' already exists! Please try another one!\n", fg=typer.colors.BRIGHT_RED)
                continue_adding_question = qt.confirm("Do you want to add more habits?").ask()
                if continue_adding_question is True:
                    continue
                else:
                    adding_is_on = False
                    for_adding_second_continue_question = qt.select("Do you want to keep editting or exit?",
                    choices=["Keep editting", "Go to Start", "Exit"],
                    ).ask()
                    if for_adding_second_continue_question == "Keep editting":
                        edit()
                    elif for_adding_second_continue_question == "Go to Start":
                        start()
                    else:
                        exit_adding_is_on = True
                        while exit_adding_is_on:
                            exit_adding_question = qt.confirm("Are you sure you want to exit ?").ask()
                            if exit_adding_question:
                                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                fg=typer.colors.BRIGHT_CYAN)
                                exit_adding_is_on = False
                                raise typer.Exit()
                            else:
                                counter_exit_adding_question = qt.select("What do you want to do?",
                                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                ).ask()
                                if counter_exit_adding_question == "Editting":
                                    edit()
                                elif counter_exit_adding_question == "Managing":
                                    manage()
                                elif counter_exit_adding_question == "Analyzing":
                                    analyze()
                                elif counter_exit_adding_question == "Go to Start":
                                    start()
                                else:
                                    exit_adding_question
            except ValueError:
                typer.secho(f"\nThere is no habit in your database ! Please add one first!\n", fg=typer.colors.BRIGHT_RED)
                raise typer.Abort()

    elif edit_question == "Delete":
        deleting_is_on = True
        db = database.connect_db()
        while deleting_is_on:
            try:
                deleting_habit_entry = operating_habit()
                if database.habit_existing_check(db, deleting_habit_entry) is True:
                    if get.delete_confirmation(deleting_habit_entry):
                        deleting_entry = model.Habit(deleting_habit_entry)
                        model.Habit.delete_habit(deleting_entry)
                        database.reset_log(db, deleting_habit_entry)
                        if len(database.all_habits(db)) > 0:
                            show(None)
                            typer.secho(f"\nThe habit '{deleting_habit_entry}' is deleted!\n", fg=typer.colors.BRIGHT_GREEN)
                                
                            continue_deleting_question = qt.confirm("Do you want to delete more habits?").ask()
                            if continue_deleting_question is True:
                                continue
                            else:
                                for_deleting_second_continue_question = qt.select("Do you want to keep editting or exit?",
                                choices=["Keep editting", "Go to Start", "Exit"],
                                ).ask()
                                for_deleting_second_continue_question
                                if for_deleting_second_continue_question == "Keep editting":
                                    edit()
                                elif for_deleting_second_continue_question == "Go to Start":
                                    start()
                                    deleting_is_on = False
                                else:
                                    exit_deleting_is_on = True
                                    while exit_deleting_is_on:
                                        exit_deleting_question = qt.confirm("Are you sure you want to exit ?").ask()
                                        if exit_deleting_question:
                                            typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                            fg=typer.colors.BRIGHT_CYAN)
                                            exit_deleting_is_on = False
                                            raise typer.Exit()
                                        else:
                                            counter_exit_deleting_question = qt.select("What do you want to do?",
                                            choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                            ).ask()
                                            if counter_exit_deleting_question == "Editting":
                                                edit()
                                            elif counter_exit_deleting_question == "Managing":
                                                manage()
                                            elif counter_exit_deleting_question == "Analyzing":
                                                analyze()
                                            elif counter_exit_deleting_question == "Go to Start":
                                                start()
                                            else:
                                                exit_deleting_question
                        else:
                            typer.secho(f"\nThe habit '{deleting_habit_entry}' is deleted!\n", fg=typer.colors.BRIGHT_GREEN)
                            typer.secho(f"\nThere are no more habits in your database that could be seen in your overview !\n",
                            fg=typer.colors.BRIGHT_RED)
                            exit_question = qt.confirm("Do you want to keep your app running and go back to start?").ask()
                            if exit_question:
                                start()
                            else:
                                exit_deleting_is_on = True
                                while exit_deleting_is_on:
                                    exit_deleting_question = qt.confirm("Are you sure you want to exit ?").ask()
                                    if exit_deleting_question:
                                        typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                        fg=typer.colors.BRIGHT_CYAN)
                                        exit_deleting_is_on = False
                                        raise typer.Exit()
                                    else:
                                        counter_exit_deleting_question = qt.select("What do you want to do?",
                                        choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                        ).ask()
                                        if counter_exit_deleting_question == "Editting":
                                            edit()
                                        elif counter_exit_deleting_question == "Managing":
                                            manage()
                                        elif counter_exit_deleting_question == "Analyzing":
                                            analyze()
                                        elif counter_exit_deleting_question == "Go to Start":
                                            start()
                                        else:
                                            exit_deleting_question
                            deleting_is_on = False
                    else:
                        typer.secho(f"\nThe habit '{deleting_habit_entry}' wont be deleted!\n", fg=typer.colors.BRIGHT_RED)
                        continue_deleting_question = qt.confirm("Do you want to delete more habits?").ask()
                        if continue_deleting_question is True:
                            continue
                        else:
                            for_deleting_second_continue_question = qt.select("Do you want to keep editting or exit?",
                            choices=["Keep editting", "Go to Start", "Exit"],
                            ).ask()
                            if for_deleting_second_continue_question == "Keep editting":
                                edit()
                            elif for_deleting_second_continue_question == "Go to Start":
                                start()
                                deleting_is_on = False
                            else:
                                exit_deleting_is_on = True
                                while exit_deleting_is_on:
                                    exit_deleting_question = qt.confirm("Are you sure you want to exit ?").ask()
                                    if exit_deleting_question:
                                        typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                        fg=typer.colors.BRIGHT_CYAN)
                                        exit_deleting_is_on = False
                                        raise typer.Exit()
                                    else:
                                        counter_exit_deleting_question = qt.select("What do you want to do?",
                                        choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                        ).ask()
                                        if counter_exit_deleting_question == "Editting":
                                            edit()
                                        elif counter_exit_deleting_question == "Managing":
                                            manage()
                                        elif counter_exit_deleting_question == "Analyzing":
                                            analyze()
                                        elif counter_exit_deleting_question == "Go to Start":
                                            start()
                                        else:
                                            exit_deleting_question
                else:
                    typer.secho(f"\nThe habit '{deleting_habit_entry}' is not existing ! Please try again !\n", fg=typer.colors.BRIGHT_RED)
                    for_deleting_second_continue_question = qt.select("Do you want to keep editting or exit?",
                    choices=["Keep editting", "Go to Start", "Exit"],
                    ).ask()
                    if for_deleting_second_continue_question == "Keep editting":
                        edit()
                    elif for_deleting_second_continue_question == "Go to Start":
                        start()
                        deleting_is_on = False
                    else:
                        exit_deleting_is_on = True
                        while exit_deleting_is_on:
                            exit_deleting_question = qt.confirm("Are you sure you want to exit ?").ask()
                            if exit_deleting_question:
                                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                fg=typer.colors.BRIGHT_CYAN)
                                exit_deleting_is_on = False
                                raise typer.Exit()
                            else:
                                counter_exit_deleting_question = qt.select("What do you want to do?",
                                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                ).ask()
                                if counter_exit_deleting_question == "Editting":
                                    edit()
                                elif counter_exit_deleting_question == "Managing":
                                    manage()
                                elif counter_exit_deleting_question == "Analyzing":
                                    analyze()
                                elif counter_exit_deleting_question == "Go to Start":
                                    start()
                                else:
                                    exit_deleting_question
            except ValueError:
                typer.secho(f"\nThere is no habit in your database! Please add one first!\n", fg=typer.colors.BRIGHT_RED)
                raise typer.Abort()

    elif edit_question == "Go to Start":
        start()

    else:
        exit_deleting_is_on = True
        while exit_deleting_is_on:
            exit_deleting_question = qt.confirm("Are you sure you want to exit ?").ask()
            if exit_deleting_question:
                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                fg=typer.colors.BRIGHT_CYAN)
                exit_deleting_is_on = False
                raise typer.Exit()
            else:
                counter_exit_deleting_question = qt.select("What do you want to do?",
                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                ).ask()
                if counter_exit_deleting_question == "Editting":
                    edit()
                elif counter_exit_deleting_question == "Managing":
                    manage()
                elif counter_exit_deleting_question == "Analyzing":
                    analyze()
                elif counter_exit_deleting_question == "Go to Start":
                    start()
                else:
                    exit_deleting_question




@app.command(short_help="Manage your habits by Checking-off")
def manage():
    manage_question = qt.select("What do you want to do?",
    choices=["Check-Off", "Go to Start", "Exit"]
    ).ask()

    if manage_question == "Check-Off":
        checking_is_on = True
        db = database.connect_db()
        while checking_is_on:
            try:
                check_off_habit = operating_habit()
                if database.periodicity_of_habit(db,check_off_habit) == "Daily":
                    habit_daily = model.Habit(check_off_habit)
                    if get.check_off_confirmation(check_off_habit):
                        if habit_daily.daily_streak_verification() == 1:
                            habit_daily.update_streak()
                            show(None)
                            typer.secho(f"\nCONGRATULATIONS ! You completed the habit '{check_off_habit}' today ! Keep it going!\n",
                            fg=typer.colors.BRIGHT_GREEN)
                        elif habit_daily.daily_streak_verification() == 0:
                            typer.secho(f"\nYou already completed this habit today ! Please try again tomorrow !\n",
                            fg=typer.colors.BRIGHT_RED)
                        else:
                            habit_daily.reset_streak()

                elif database.periodicity_of_habit(db,check_off_habit) == "Weekly":
                    habit_weekly = model.Habit(check_off_habit)
                    if get.check_off_confirmation(check_off_habit):
                        if habit_weekly.weekly_streak_verification() == 2:
                            database.complete_habit(db,check_off_habit)
                            habit_weekly.check_habit_off()
                            show(None)
                            typer.secho(f"\nCONGRATULATIONS ! You completed the habit '{check_off_habit}' this week ! Keep it going!\n",
                            fg=typer.colors.BRIGHT_GREEN)
                        elif habit_weekly.weekly_streak_verification() == 1:
                            typer.secho(f"\nYou already completed this habits this week ! Please try again next week !\n",
                            fg=typer.colors.BRIGHT_RED)
                        else:
                            habit_weekly.reset_streak()

                check_off_continue_question = qt.confirm("Do you want to check off more habits ?").ask()
                if check_off_continue_question is True:
                    continue
                else:
                    checking_is_on = False
                    for_check_off_second_question = qt.select("Do you want to keep on managing or exit?",
                    choices=["Keep managing", "Go to Start", "Exit"],
                    ).ask()
                    
                    if for_check_off_second_question == "Keep managing":
                        manage()
                    elif for_check_off_second_question == "Go to Start":
                        start()
                    else:
                        exit_checkoff_is_on = True
                        while exit_checkoff_is_on:
                            exit_checkoff_question = qt.confirm("Are you sure you want to exit ?").ask()
                            if exit_checkoff_question:
                                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                fg=typer.colors.BRIGHT_CYAN)
                                exit_checkoff_is_on = False
                                raise typer.Exit()
                            else:
                                counter_exit_checkoff_question = qt.select("What do you want to do?",
                                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                ).ask()
                                if counter_exit_checkoff_question == "Editting":
                                    edit()
                                elif counter_exit_checkoff_question == "Managing":
                                    manage()
                                elif counter_exit_checkoff_question == "Analyzing":
                                    analyze()
                                elif counter_exit_checkoff_question == "Go to Start":
                                    start()
                                else:
                                    exit_checkoff_question

            except ValueError:
                typer.secho(f"\nThere are no habits in your database ! Please add one first !",
                fg=typer.colors.BRIGHT_RED)
                raise typer.Abort()


    elif manage_question == "Go to Start":
        start()

    else:
        exit_checkoff_is_on = True
        while exit_checkoff_is_on:
            exit_checkoff_question = qt.confirm("Are you sure you want to exit ?").ask()
            if exit_checkoff_question:
                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                fg=typer.colors.BRIGHT_CYAN)
                exit_checkoff_is_on = False
                raise typer.Exit()
            else:
                counter_exit_checkoff_question = qt.select("What do you want to do?",
                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                ).ask()
                if counter_exit_checkoff_question == "Editting":
                    edit()
                elif counter_exit_checkoff_question == "Managing":
                    manage()
                elif counter_exit_checkoff_question == "Analyzing":
                    analyze()
                elif counter_exit_checkoff_question == "Go to Start":
                    start()
                else:
                    exit_checkoff_question
        

@app.command(short_help="Analyze your habits")
def analyze():
    analyze_question = qt.select("What do you want to analyze?",
    choices=["All currently tracked habits", "All habits with same periodicity", "Longest streak - All habits",
    "Longest streak - Given habit", "Exit"],
    ).ask()

    if analyze_question == "All currently tracked habits":
        db = database.connect_db()
        try:
            habits_analyze_data = analytics.all_habits_information(db)
            if len(habits_analyze_data) > 0:
                show(None)
                typer.secho("\nThese are all habits that are currently tracked for you !\n",
                fg=typer.colors.BRIGHT_GREEN)
                all_habits_analyze_question = qt.select("What do you want to do?",
                choices=["Editting", "Managing", "Analyzing","Exit"],
                ).ask()
                if all_habits_analyze_question == "Editting":
                    edit()
                elif all_habits_analyze_question == "Managing":
                    manage()
                elif all_habits_analyze_question == "Analyzing":
                    analyze()
                else:
                    exit_analyzing_all_is_on = True
                    while exit_analyzing_all_is_on:
                        exit_analyzing_all_question = qt.confirm("You're leaving the app ! Are you sure you want to exit ?").ask()
                        if exit_analyzing_all_question:
                            typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                            fg=typer.colors.BRIGHT_CYAN)
                            exit_analyzing_all_is_on = False
                            raise typer.Exit()
                        else:
                            counter_exit_analyzing_all_question = qt.select("What do you want to do?",
                            choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                            ).ask()
                            if counter_exit_analyzing_all_question == "Editting":
                                edit()
                            elif counter_exit_analyzing_all_question == "Managing":
                                manage()
                            elif counter_exit_analyzing_all_question == "Analyzing":
                                analyze()
                            elif counter_exit_analyzing_all_question == "Go to Start":
                                start()
                            else:
                                exit_analyzing_all_question
            else:
                typer.secho("\nThere are no habits that are currently tracked !\n",
                fg=typer.colors.BRIGHT_RED)
                start_editting_question = qt.confirm("Do you want to start editting and add a habit?").ask()
                if start_editting_question:
                    edit()
                else:
                    exit_all_habits_is_on = True
                    while exit_all_habits_is_on:
                        exit_all_habits_question = qt.confirm("You're leaving the app ! Are you sure you want to exit ?").ask()
                        if exit_all_habits_question:
                            typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                            fg=typer.colors.BRIGHT_CYAN)
                            exit_is_on = False
                            raise typer.Exit()
                        else:
                            counter_all_habits_exit_question = qt.select("What do you want to do?",
                            choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                            ).ask()
                            if counter_all_habits_exit_question == "Editting":
                                edit()
                            elif counter_all_habits_exit_question == "Managing":
                                manage()
                            elif counter_all_habits_exit_question == "Analyzing":
                                analyze()
                            elif counter_all_habits_exit_question == "Go to Start":
                                start()
                            else:
                                exit_all_habits_question
        except TypeError:
            typer.secho(f"\nThere is no habit in your database ! Please add one first!\n", fg=typer.colors.BRIGHT_RED)
            raise typer.Abort()

    elif analyze_question == "All habits with same periodicity":
        db = database.connect_db()
        try:
            periodicity_analyze_name = get_periodicity_name()
            if len(analytics.habit_custom_perdiodicity_information(db, periodicity_analyze_name)) > 0 :
                if periodicity_analyze_name == "Daily":
                    show(periodicity="Daily")
                    typer.secho(f"\nHere is an overview of your habits with the periodicity '{periodicity_analyze_name}' !\n",
                    fg=typer.colors.BRIGHT_GREEN)
                    analyze_continue_question = qt.select("Do you want to keep analyzing?",
                    choices=["Keep analyzing", "Go to Start", "Exit"],
                    ).ask()
                    if analyze_continue_question == "Keep analyzing":
                        analyze()
                    elif analyze_continue_question == "Go to Start":
                        start()
                    else:
                        exit_analyzing_daily_is_on = True
                        while exit_analyzing_daily_is_on:
                            exit_analyzing_daily_question = qt.confirm("You're leaving the app ! Are you sure you want to exit ?").ask()
                            if exit_analyzing_daily_question:
                                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                fg=typer.colors.BRIGHT_CYAN)
                                exit_analyzing_daily_is_on = False
                                raise typer.Exit()
                            else:
                                counter_exit_analyzing_daily_question = qt.select("What do you want to do?",
                                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                ).ask()
                                if counter_exit_analyzing_daily_question == "Editting":
                                    edit()
                                elif counter_exit_analyzing_daily_question == "Managing":
                                    manage()
                                elif counter_exit_analyzing_daily_question == "Analyzing":
                                    analyze()
                                elif counter_exit_analyzing_daily_question == "Go to Start":
                                    start()
                                else:
                                    exit_analyzing_daily_question
                elif periodicity_analyze_name =="Weekly":
                    show(periodicity="Weekly")
                    typer.secho(f"\nHere is an overview of your habits with the periodicity '{periodicity_analyze_name}' !\n",
                    fg=typer.colors.BRIGHT_GREEN)
                    analyze_continue_question = qt.select("Do you want to keep analyzing?",
                    choices=["Keep analyzing", "Go to Start", "Exit"],
                    ).ask()
                    if analyze_continue_question == "Keep analyzing":
                        analyze()
                    elif analyze_continue_question == "Go to Start":
                        start()
                    else:
                        exit_analyzing_weekly_is_on = True
                        while exit_analyzing_weekly_is_on:
                            exit_analyzing_weekly_question = qt.confirm("You're leaving the app ! Are you sure you want to exit ?").ask()
                            if exit_analyzing_weekly_question:
                                typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                                fg=typer.colors.BRIGHT_CYAN)
                                exit_analyzing_weekly_is_on = False
                                raise typer.Exit()
                            else:
                                counter_exit_analyzing_weekly_question = qt.select("What do you want to do?",
                                choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                                ).ask()
                                if counter_exit_analyzing_weekly_question == "Editting":
                                    edit()
                                elif counter_exit_analyzing_weekly_question == "Managing":
                                    manage()
                                elif counter_exit_analyzing_weekly_question == "Analyzing":
                                    analyze()
                                elif counter_exit_analyzing_weekly_question == "Go to Start":
                                    start()
                                else:
                                    exit_analyzing_weekly_question
                else:
                    typer.secho(f"\nNo matching habits with the periodicity '{periodicity_analyze_name}' found in your database!\n",
                    fg=typer.colors.BRIGHT_RED)
            else:
                typer.secho(f"\nThere are no habits with the periodicity '{periodicity_analyze_name}' in your database !\n",
                fg=typer.colors.BRIGHT_RED)
                adding_question = qt.confirm("Do you want to start editting and add a habit ?").ask()
                if adding_question:
                    edit()
                else:
                    exit_is_on = True
                    while exit_is_on:
                        exit_question = qt.confirm("You're leaving the app ! Are you sure you want to exit ?").ask()
                        if exit_question:
                            typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
                            fg=typer.colors.BRIGHT_CYAN)
                            exit_is_on = False
                            raise typer.Exit()
                        else:
                            counter_exit_question = qt.select("What do you want to do?",
                            choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
                            ).ask()
                            if counter_exit_question == "Editting":
                                edit()
                            elif counter_exit_question == "Managing":
                                manage()
                            elif counter_exit_question == "Analyzing":
                                analyze()
                            elif counter_exit_question == "Go to Start":
                                start()
                            else:
                                exit_question
        except TypeError:
            typer.secho(f"\nThere is no habit in your database ! Please add one first!\n", fg=typer.colors.BRIGHT_RED)
            raise typer.Abort()




if __name__ == "__main__":
    app()