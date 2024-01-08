from pymongo import MongoClient

from GymProProject.pymongo_get_database import get_database


class Routine:
    """
    Represents a workout routine.

    Attributes:
        name (str): The name of the routine.
        exercises_in_routine (list): List of exercises in the routine, each represented as a dictionary with 'exercise_id' and 'sets'.

    Methods:
        to_dict(): Converts the routine object to a dictionary.
        from_dict(routine_data): Creates a Routine object from a dictionary.
    """

    def __init__(self, name, exercises_in_routine=None):
        self.name = name
        self.exercises_in_routine = exercises_in_routine or []

    def to_dict(self):
        return {
            "name": self.name,
            "exercises_in_routine": [
                {"exercise_id": exercise["exercise_id"], "sets": exercise["sets"]}
                for exercise in self.exercises_in_routine
            ]
        }

    @staticmethod
    def from_dict(routine_data):
        name = routine_data.get("name")
        exercises_data = routine_data.get("exercises_in_routine", [])
        exercises_in_routine = [
            {"exercise_id": exercise["exercise_id"], "sets": exercise["sets"]}
            for exercise in exercises_data
        ]
        return Routine(name, exercises_in_routine)


class Workout:
    """
    Represents a user's workout session.

    Attributes:
        date (str): The date of the workout.
        title (str): The title of the workout.
        exercises (list): List of exercises in the workout, each represented as a dictionary with 'exercise_id' and 'sets'.

    Methods:
        add_exercise(exercise_id, sets): Adds a new exercise to the workout.
        to_dict(): Converts the workout object to a dictionary.
        from_dict(workout_data): Creates a Workout object from a dictionary.
    """

    def __init__(self, date, title, exercises=None):
        self.date = date
        self.title = title
        self.exercises = exercises or []

    def add_exercise(self, exercise_id, sets):
        self.exercises.append({"exercise_id": exercise_id, "sets": sets})

    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date,
            "exercises_in_workout": [
                {"exercise_id": exercise["exercise_id"], "sets": exercise["sets"]}
                for exercise in self.exercises
            ]
        }

    @staticmethod
    def from_dict(workout_data):
        title = workout_data.get("title")
        date = workout_data.get("date")
        exercises_data = workout_data.get("exercises_in_workout", [])
        exercises = [
            {"exercise_id": exercise["exercise_id"], "sets": exercise["sets"]}
            for exercise in exercises_data
        ]
        return Workout(date, title, exercises)


class User:
    """
    Represents a user with routines and workout history.

    Attributes:
        name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        routines (list): List of Routine objects.
        workouts (list): List of Workout objects.

    Methods:
        add_routine(routine): Adds a routine to the user's list.
        remove_routine(routine): Removes a routine from the user's list.
        update_name(new_name): Updates the user's name.
        update_email(new_email): Updates the user's email.
        update_password(new_password): Updates the user's password.
        add_workout(workout): Adds a workout to the user's list.
        remove_workout(workout): Removes a workout from the user's list.
        get_exercise_history(exercise_id): Returns the workout history for a specific exercise.
        get_all_exercise_details(): Retrieves details for all exercises in the user's workouts.
        to_dict(): Converts the user object to a dictionary.
        from_dict(data): Creates a User object from a dictionary.
    """

    def __init__(self, name, email, password, routines=None, workouts=None):
        self.name = name
        self.email = email
        self.password = password
        self.routines = routines or []
        self.workouts = workouts or []
        self.db = get_database()

    def add_routine(self, routine):
        self.routines.append(routine)
        self.db.users.update_one({"email": self.email},
                                 {"$push": {"routines": routine.to_dict()}})

    def remove_routine(self, routine):
        self.routines.remove(routine)
        self.db.users.update_one({"email": self.email},
                                 {"$pull": {"routines": {"name": routine.name}}})

    def update_name(self, new_name):
        self.name = new_name
        self.db.users.update_one({"email": self.email}, {"$set": {"name": new_name}})

    def update_email(self, new_email):
        self.db.users.update_one({"email": self.email}, {"$set": {"email": new_email}})
        self.email = new_email

    def update_password(self, new_password):
        self.password = new_password
        self.db.users.update_one({"email": self.email}, {"$set": {"password": new_password}})

    def add_workout(self, workout):
        self.workouts.append(workout)
        self.db.users.update_one(
            {"email": self.email},
            {"$push": {"workouts": workout.to_dict()}}
        )

    def remove_workout(self, workout):
        self.workouts.remove(workout)
        self.db.users.update_one({"email": self.email},
                                 {"$pull": {"workouts": {"date": workout.date}}})

    def get_exercise_history(self, exercise_id):
        # Search through workouts for the given exercise_id
        history = []
        for workout in self.workouts:
            for exercise in workout.exercises:
                if exercise["exercise_id"] == exercise_id:
                    history.append({"title": workout.title, "date": workout.date, "sets": exercise["sets"]})
        return history

    def get_all_exercise_details(self):
        exercise_ids = []
        for workout in self.workouts:
            exercise_ids = [exercise["exercise_id"] for exercise in workout.exercises]
        if exercise_ids:
            exercise_details = list(self.db.exercises.find({"id": {"$in": exercise_ids}}))
            return exercise_details
        return print("No exercises")

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "routines": [routine.to_dict() for routine in self.routines],
            "workouts": [workout.to_dict() for workout in self.workouts],
        }

    @staticmethod
    def from_dict(data):
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        routines_data = data.get("routines", [])
        workouts_data = data.get("workouts", [])

        routines = [Routine.from_dict(routine_data) for routine_data in routines_data]
        workouts = [Workout.from_dict(workout_data) for workout_data in workouts_data]

        return User(name, email, password, routines, workouts)
