import streamlit as st
import csv

CSV_FILE = "tasks.csv"


def main():
    st.title("📝 To-Do List")

    # Apply background styling
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.pexels.com/photos/2387793/pexels-photo-2387793.jpeg?cs=srgb&dl=pexels-adrien-olichon-2387793.jpg&fm=jpg");
            background-attachment: fixed;
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    task_list = load_tasks()
    display_tasks(task_list)

    task_input = st.text_input("Add a new task:")
    if st.button("Add"):
        if task_input.strip():  # Fixed: use strip() instead of != ""
            task_list.append(task_input.strip())
            save_tasks(task_list)
            st.rerun()  # Fixed: refresh page to clear input

    # Fixed: Move selectbox inside proper condition
    if task_list:  # Only show if tasks exist
        selected_task = st.selectbox("Select a task to remove:", options=task_list)
        if st.button("Delete"):
            delete(task_list, selected_task)
            st.rerun()  # Fixed: refresh after deletion

    if st.button("Clear all tasks"):
        if task_list:  # Only clear if tasks exist
            task_list.clear()
            save_tasks(task_list)
            st.rerun()
        else:
            st.info("No tasks to clear.")


def load_tasks():
    try:
        with open(CSV_FILE, "r") as f:  # Fixed: added space
            reader = csv.reader(f)
            return [row[0] for row in reader if row]  # Fixed: check if row exists
    except FileNotFoundError:
        return []


def display_tasks(task_list):
    if not task_list:  # More pythonic
        st.info("No tasks added yet.")  # Fixed: typo "tasts" -> "tasks", use st.info
    else:
        st.success("Current tasks:")  # Better visual feedback
        for i, task in enumerate(task_list, 1):  # Start from 1 directly
            st.write(f"{i}. {task}")


def save_tasks(task_list):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([[task] for task in task_list])


def delete(task_list, selected_task):
    if selected_task in task_list:  # Add safety check
        task_list.remove(selected_task)
        save_tasks(task_list)
        st.success(f"Task '{selected_task}' deleted successfully!")
    else:
        st.error("Task not found.")


# Run the app
if __name__ == "__main__":
    main()
