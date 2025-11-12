from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import re


def create_app() -> Flask:
    """Application factory for the Expense Splitter Flask app."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            # Get form data
            try:
                total_amount = float(request.form.get("total_amount", 0))
                num_people = int(request.form.get("num_people", 0))
            except (ValueError, TypeError):
                return render_template(
                    "index.html",
                    error="Invalid total amount or number of people.",
                )

            # Collect person data
            people = []
            names = []
            emails = []
            contributions = {}

            for i in range(1, num_people + 1):
                name = request.form.get(f"name_{i}", "").strip()
                email = request.form.get(f"email_{i}", "").strip().lower()
                contribution_str = request.form.get(f"contribution_{i}", "").strip()

                if name or email:
                    # Validate unique name
                    if name and name in names:
                        return render_template(
                            "index.html",
                            error=f"Duplicate name found: {name}. Names must be unique.",
                        )

                    # Validate unique email
                    if email and email in emails:
                        return render_template(
                            "index.html",
                            error=f"Duplicate email found: {email}. Emails must be unique.",
                        )

                    # Validate email format if provided
                    if email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                        return render_template(
                            "index.html",
                            error=f"Invalid email format: {email}",
                        )

                    # Parse contribution
                    contribution = 0.0
                    if contribution_str:
                        try:
                            contribution = float(contribution_str)
                            if contribution < 0:
                                return render_template(
                                    "index.html",
                                    error=f"Contribution cannot be negative for {name or email or f'Person {i}'}",
                                )
                        except ValueError:
                            return render_template(
                                "index.html",
                                error=f"Invalid contribution amount for {name or email or f'Person {i}'}",
                            )

                    people.append({
                        "name": name or f"Person {i}",
                        "email": email,
                        "contribution": contribution,
                    })
                    if name:
                        names.append(name)
                    if email:
                        emails.append(email)
                    contributions[name or email or f"Person {i}"] = contribution

            if not people:
                return render_template(
                    "index.html",
                    error="Please provide at least one person with a name or email.",
                )

            # Calculate expense split
            results = calculate_expense_split(total_amount, people)

            return render_template(
                "index.html",
                results=results,
                total_amount=total_amount,
                num_people=num_people,
                people=people,
            )

        return render_template("index.html")

    return app


def calculate_expense_split(total_amount: float, people: list) -> dict:
    """
    Calculate who owes or gets back money.
    
    Returns a dictionary with:
    - 'per_person': amount each person should pay
    - 'transactions': list of who owes whom and how much
    - 'summary': list of each person's status (owes/gets back)
    """
    num_people = len(people)
    per_person = total_amount / num_people if num_people > 0 else 0

    # Calculate what each person has paid vs what they should pay
    balances = {}
    for person in people:
        person_id = person["name"]
        paid = person["contribution"]
        should_pay = per_person
        balance = paid - should_pay
        balances[person_id] = balance

    # Separate creditors (who gets money back) and debtors (who owes money)
    creditors = {name: amount for name, amount in balances.items() if amount > 0.01}
    debtors = {name: -amount for name, amount in balances.items() if amount < -0.01}

    # Calculate transactions (simplified: match largest debts with largest credits)
    transactions = []
    creditor_list = sorted(creditors.items(), key=lambda x: x[1], reverse=True)
    debtor_list = sorted(debtors.items(), key=lambda x: x[1], reverse=True)

    creditor_idx = 0
    debtor_idx = 0

    while creditor_idx < len(creditor_list) and debtor_idx < len(debtor_list):
        creditor_name, creditor_amount = creditor_list[creditor_idx]
        debtor_name, debtor_amount = debtor_list[debtor_idx]

        if creditor_amount < 0.01:
            creditor_idx += 1
            continue
        if debtor_amount < 0.01:
            debtor_idx += 1
            continue

        # Calculate how much to transfer
        transfer_amount = min(creditor_amount, debtor_amount)
        transactions.append({
            "from": debtor_name,
            "to": creditor_name,
            "amount": round(transfer_amount, 2),
        })

        # Update balances
        creditor_amount -= transfer_amount
        debtor_amount -= transfer_amount

        creditor_list[creditor_idx] = (creditor_name, creditor_amount)
        debtor_list[debtor_idx] = (debtor_name, debtor_amount)

        if creditor_amount < 0.01:
            creditor_idx += 1
        if debtor_amount < 0.01:
            debtor_idx += 1

    # Create summary
    summary = []
    for person in people:
        person_id = person["name"]
        balance = balances.get(person_id, 0)
        if abs(balance) < 0.01:
            summary.append({
                "name": person_id,
                "status": "settled",
                "amount": 0,
            })
        elif balance > 0:
            summary.append({
                "name": person_id,
                "status": "gets_back",
                "amount": round(balance, 2),
            })
        else:
            summary.append({
                "name": person_id,
                "status": "owes",
                "amount": round(-balance, 2),
            })

    return {
        "per_person": round(per_person, 2),
        "transactions": transactions,
        "summary": summary,
    }


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)

