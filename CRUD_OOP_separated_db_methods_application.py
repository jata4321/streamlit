import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "sqlite:///./databases/test_oop_sep_meth.db3"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Generic Data Access Class
class DataAccess:
    @staticmethod
    def add_item(session, model, **kwargs):
        new_item = model(**kwargs)
        session.add(new_item)
        session.commit()

    @staticmethod
    def get_all_items(session, model):
        return session.query(model).all()

    @staticmethod
    def update_item(session, model, item_id, **kwargs):
        item = session.query(model).filter(model.id == item_id).first()
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            session.commit()

    @staticmethod
    def delete_item(session, model, item_id):
        item = session.query(model).filter(model.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()


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

    with SessionLocal() as session:
        # Create
        if choice == "Create":
            st.subheader("Add Item")
            name = st.text_input("Name")
            description = st.text_area("Description")

            if st.button("Add Item"):
                DataAccess.add_item(session, Item, name=name, description=description)
                st.success("Item added successfully")

        # Read
        elif choice == "Read":
            st.subheader("View Items")
            items = DataAccess.get_all_items(session, Item)
            for item in items:
                st.write(f"ID: {item.id}, Name: {item.name}, Description: {item.description}")

        # Update
        elif choice == "Update":
            st.subheader("Update Item")
            items = DataAccess.get_all_items(session, Item)
            item_dict = {item.name: item.id for item in items}
            selected_item = st.selectbox("Select an Item to Update", list(item_dict.keys()))

            name = st.text_input("New Name")
            description = st.text_area("New Description")

            if st.button("Update Item"):
                item_id = item_dict[selected_item]
                DataAccess.update_item(session, Item, item_id, name=name, description=description)
                st.success("Item updated successfully")

        # Delete
        elif choice == "Delete":
            st.subheader("Delete Item")
            items = DataAccess.get_all_items(session, Item)
            item_dict = {item.name: item.id for item in items}
            selected_item = st.selectbox("Select an Item to Delete", list(item_dict.keys()))

            if st.button("Delete Item"):
                item_id = item_dict[selected_item]
                DataAccess.delete_item(session, Item, item_id)
                st.success("Item deleted successfully")


if __name__ == "__main__":
    main()