import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "sqlite:///./databases/test.db3"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database models
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


# Create database tables
Base.metadata.create_all(bind=engine)


# Streamlit app
def main():
    st.title("CRUD App using Streamlit and SQLAlchemy")

    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Create
    if choice == "Create":
        st.subheader("Add Item")
        name = st.text_input("Name")
        description = st.text_area("Description")

        if st.button("Add Item"):
            with SessionLocal() as session:
                new_item = Item(name=name, description=description)
                session.add(new_item)
                session.commit()
            st.success("Item added successfully")

    # Read
    elif choice == "Read":
        st.subheader("View Items")
        with SessionLocal() as session:
            items = session.query(Item).all()
            for item in items:
                st.write(f"ID: {item.id}, Name: {item.name}, Description: {item.description}")

    # Update
    elif choice == "Update":
        st.subheader("Update Item")
        with SessionLocal() as session:
            items = session.query(Item).all()
            item_dict = {item.name: item.id for item in items}
            selected_item = st.selectbox("Select an Item to Update", list(item_dict.keys()))

            name = st.text_input("New Name")
            description = st.text_area("New Description")

            if st.button("Update Item"):
                item_id = item_dict[selected_item]
                item = session.query(Item).filter(Item.id == item_id).first()
                item.name = name
                item.description = description
                session.commit()
                st.success("Item updated successfully")

    # Delete
    elif choice == "Delete":
        st.subheader("Delete Item")
        with SessionLocal() as session:
            items = session.query(Item).all()
            item_dict = {item.name: item.id for item in items}
            selected_item = st.selectbox("Select an Item to Delete", list(item_dict.keys()))

            if st.button("Delete Item"):
                item_id = item_dict[selected_item]
                item = session.query(Item).filter(Item.id == item_id).first()
                session.delete(item)
                session.commit()
                st.success("Item deleted successfully")


if __name__ == "__main__":
    main()