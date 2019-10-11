import re

from configparser import ConfigParser

REPLACEMENT_REGEX = '{([^{}]+)}'
CONDITIONAL_REGEX = '<[^<>]+>'
CONDITION_REGEX = '\[(([^[\]]*)\(([^[\]]*)\))?\]([^[\]<>]*)'


class CoverLetter:
    """ Holds functionality for generating a cover letter given a config. """

    def __init__(self, config):
        self.position = config['POSITION']
        self.info = config['INFO']
        self.templates = config['TEMPLATES']

    def _skill_list(self, key):
        """ Given a skill key, generate a comma separated list of the common skills. """

        position_skills = self.position[key].split(', ')
        info_skills = self.info[key].split(', ')

        # Only use skills that are present in both lists.
        intersection = [skill for skill in position_skills if skill in info_skills]
        if not intersection:
            return 'nothing'

        # Make a comma separated list with an "and" at the end.
        return ', '.join(intersection[:-1]) + ', and ' + intersection[-1]

    def _lookup(self, key):
        """ Lookup a key in the config. """

        if key in self.position and key in self.info:
            # If the key exists in both position and info, treat it as a list to intersect.
            return self._skill_list(key)
        if key in self.position:
            return self.position[key]
        if key in self.info:
            return self.info[key]

        raise KeyError(f"Invalid Key: {key}")

    def generate(self):
        """ Generate and return the cover letter. """

        letter = ''

        for template_name in self.templates:
            template = self.templates[template_name]

            # Process all replacements ({...} syntax).
            replacements = re.finditer(REPLACEMENT_REGEX, template)
            for replacement in replacements:
                match = replacement.group()
                key = replacement.group(1)

                template = template.replace(match, self._lookup(key))

            # Process all conditionals (<...> syntax).
            conditionals = re.finditer(CONDITIONAL_REGEX, template)
            for conditional in conditionals:
                match = conditional.group()

                # Process each condition within the conditional ([...]... syntax).
                conditions = re.finditer(CONDITION_REGEX, match)
                for index, condition in enumerate(conditions):
                    skill_type = condition.group(2)
                    skill = condition.group(3)
                    text = condition.group(4)

                    # If the skill is empty, treat it as a catch all case.
                    if not skill or skill in self._lookup(skill_type):
                        template = template.replace(match, text)
                        break

            letter += template

        return letter


def main():
    config = ConfigParser()
    config.read('config.ini')

    cover_letter = CoverLetter(config)

    with open('coverletter-template.html', 'r') as template_file:
        template = template_file.read()

    with open('coverletter.html', 'w') as file:
        file.write(template.replace('{Coverletter}', cover_letter.generate()))


if __name__ == '__main__':
    main()
