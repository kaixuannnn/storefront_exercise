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

# Validate Deserializing Data

# Save the validated data in to database, update the existing data in database

# Model View set

- sometimes we might see the queryset and serializer are repeated, to reduce the redundancy, we can use viewset
- For modelViewSet, we cn perform all kind of HTTP request, create, update, read destory and so
- If we only want to read only, we can use ReadOnlyModelViewSet
