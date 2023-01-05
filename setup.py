import setuptools
import toml

with open("pyproject.toml") as f:
    pyproject = toml.load(f)

metadata = pyproject["metadata"]
setuptools_requires = pyproject["setuptools_requires"]
options = pyproject.get("options", {})
entry_points = pyproject.get("entry_points", {})

setuptools.setup(
    name=metadata["name"],
    version=metadata["version"],
    author=metadata["author"],
    author_email=metadata["author_email"],
    description=metadata["description"],
    long_description=metadata.get("long_description", ""),
    long_description_content_type=metadata.get("long_description_content_type", ""),
    url=metadata.get("url", ""),
    classifiers=metadata.get("classifiers", []),
    python_requires=metadata.get("python_requires", ""),
    setuptools_requires=setuptools_requires,
    packages=options.get("packages", []),
    entry_points=entry_points,
)
