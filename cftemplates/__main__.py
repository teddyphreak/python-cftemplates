from cftemplates import vpc


def create_templates():
    vpc_template = vpc.vpc_template(description="Master VPC template")
    with open('vpc.template', 'w') as f:
        f.truncate()
        f.write(vpc_template)


def main():
    create_templates()


if __name__ == '__main__':
    main()
