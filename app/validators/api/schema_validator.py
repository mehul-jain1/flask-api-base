import re


class SchemaValidator(object):
    def __init__(self, post_data={}):
        self.post_data = post_data

    def validate_user_schema(self):
        errors = []

        try:
            if not self.post_data:
                errors.append("please provide a valid user schema")
                return errors

            # name validation
            name = self.post_data.get("name", None)
            if not name or name == "":
                errors.append("user name is required")
                return errors

            # email validation
            email = self.post_data.get("email", None)
            if not email or email == "":
                errors.append("email is required")
                return errors
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("invalid email address")
                return errors
            # role validation
            role = self.post_data.get("role", None)
            if not role or role == "":
                errors.append("role is required")
                return errors
            if role not in ["manager", "agent"]:
                errors.append("invalid role")
                return errors
        except Exception as e:
            errors.append(format(e))

        return errors

    def validate_upload_schema(self):
        errors = []
        try:
            # validate files schema
            if len(self.post_data) == 0:
                errors.append("Please use atleast one type to upload files")
                return errors

            err = []
            for key in self.post_data:
                for filename in self.post_data[key]:
                    if filename == "":
                        err.append(key)

            if len(err) > 0:
                errors.append("Please select files to upload for " + ", ".join(err))

        except Exception as e:
            errors.append(format(e))

        return errors
