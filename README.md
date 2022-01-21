# storefront_exercise

# Extending Pluggable Apps

- We dont want tag and store app rely on each other, so create a custom app to connect them
- When the custom app is removed , tag and store app can run nicely

# Serializer

# Create Custom Serializer Fields

- API Model doesnt necesssary need to look exactly the same as Data Model

# Serializing Relationships

- another way to do is doing in nested way
- another way we can do is add a hyperlink
- conclude, we have 4 ways ro serialize the relationships: primary_key, string, nested object, hyperlink

# Model Serializer

- As you can see, we have 2 place on validating and defining our field
- So we can use modelSerializer to avoid the duplication
- ModelSerializer by default using primarykey related fields
- if the definition is not what we want we can serialize it like before we do

# Deserializing Objects

- POST
