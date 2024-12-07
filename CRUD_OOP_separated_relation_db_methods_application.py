import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Database setup
DATABASE_URL = "sqlite:///./databases/test_oop_sep_rel_meth.db3"

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
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="items")


# Create database tables
Base.metadata.create_all(bind=engine)


# Streamlit app
def main():
    st.title("CRUD App for Items and Categories")

    menu = ["Create Category", "Create Item", "Read Items", "Update Item", "Delete Item"]
    choice = st.sidebar.selectbox("Menu", menu)

    with SessionLocal() as session:
        # Create Category
        if choice == "Create Category":
            st.subheader("Add Category")
            category_name = st.text_input("Category Name")

            if st.button("Add Category"):
                DataAccess.add_item(session, Category, name=category_name)
                st.success("Category added successfully")

        # Create Item
        elif choice == "Create Item":
            st.subheader("Add Item")
            name = st.text_input("Name")
            description = st.text_area("Description")

            categories = DataAccess.get_all_items(session, Category)
            category_dict = {category.name: category.id for category in categories}
            selected_category = st.selectbox("Select a Category", list(category_dict.keys()))

            if st.button("Add Item"):
                category_id = category_dict[selected_category]
                DataAccess.add_item(session, Item, name=name, description=description, category_id=category_id)
                st.success("Item added successfully")

        # Read Items
        elif choice == "Read Items":
            st.subheader("View Items")
            items = DataAccess.get_all_items(session, Item)
            for item in items:
                category_name = item.category.name if item.category else "No Category"
                st.write(
                    f"ID: {item.id}, Name: {item.name}, Description: {item.description}, Category: {category_name}")

        # Update Item
        elif choice == "Update Item":
            st.subheader("Update Item")
            items = DataAccess.get_all_items(session, Item)
            item_dict = {item.name: item.id for item in items}
            selected_item = st.selectbox("Select an Item to Update", list(item_dict.keys()))

            name = st.text_input("New Name")
            description = st.text_area("New Description")

            categories = DataAccess.get_all_items(session, Category)
            category_dict = {category.name: category.id for category in categories}
            selected_category = st.selectbox("Select a New Category", list(category_dict.keys()))

            if st.button("Update Item"):
                item_id = item_dict[selected_item]
                category_id = category_dict[selected_category]
                DataAccess.update_item(session, Item, item_id, name=name, description=description,
                                       category_id=category_id)
                st.success("Item updated successfully")

        # Delete Item
        elif choice == "Delete Item":
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