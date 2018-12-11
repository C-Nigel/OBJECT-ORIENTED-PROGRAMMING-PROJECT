from flask import *



app = Flask(__name__)


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/Donor', methods = ('GET','POST'))
def donor():
        if request.method == 'POST':
            item = request.form['item']
            expiry =request.form['expiry']
            quantity =request.form['quantity']
            error = None
            if not item:
                error = 'Item is required'
            elif not expiry:
                error = 'Expiry is required'
            elif not quantity:
                error = 'Quantity is required'

            else:
                donation_list = get_item(item, expiry, quantity)
                return redirect(url_for('Donor'))

        return render_template('Donor.html')




@app.route('/Donor')
def Donor1():
    # logic
    return render_template('Donor.html')

@app.route('/DonorSubmit')
def DonorSubmit2():
    return render_template('DonorSubmit.html')













if __name__ == '__main__':
    app.run()
