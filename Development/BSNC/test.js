const pdfFillForm = require('pdf-fill-form');
const readline = require('readline');
const mysql = require('mysql2');
const util = require('util')
const fs = require('fs');

const connection = mysql.createConnection({
  host: '149.28.139.83',
  user: 'sharedAccount',
  password: 'Shared536442.',
  database: 'crm_002_db',
  port: 3306
})

connection.connect((error) => {
  if (error) {
    console.log(error);
    return;
  }

})

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

rl.question("Enter a NRIC for further action : ", async (nric) => {
  const query = `SELECT * FROM \`Personal Info\`
  JOIN \`Banking Info\` ON \`Personal Info\`.NRIC = \`Banking Info\`.NRIC
  JOIN \`Extra Info\` ON \`Personal Info\`.NRIC = \`Extra Info\`.NRIC
  JOIN \`Product Info\` ON \`Personal Info\`.NRIC = \`Product Info\`.NRIC
  JOIN \`Working Info\` ON \`Personal Info\`.NRIC = \`Working Info\`.NRIC
  WHERE \`Personal Info\`.NRIC = ${nric} LIMIT 1;`;

  connection.query(query, async (error, results) => {
    if (error) {
      console.log(error);
      return;
    }
    const getReferenceContact = () => {
      return new Promise((resolve, reject) => {
        const query = `SELECT * FROM \`Reference Contact\` WHERE NRIC = ${nric} LIMIT 2;`;
        connection.query(query, (error, results) => {
          if (error) {
            console.log(error);
            reject(error);
          } else {
            resolve(results);
          }
        });
      });
    };

    let referenceContact = await getReferenceContact();
    const checkOwnershipStatus = (status) => {
      if (status.includes('own')) {
        return 'Own'; s
      } else if (status.includes('rent')) {
        return 'Rented';
      } else if (status.includes('parent')) {
        return 'Parent';
      } else {
        return 'Other';
      }

    }

    fields = results[0];

    const regex = /^(\d+,\s.+,\s.+),\s(\d+),\s(.+),\s(.+)$/;
    const date1 = new Date(fields['When user joined company']);
    const date2 = new Date();

    let totalMonths = (date2.getFullYear() - date1.getFullYear()) * 12 + (date2.getMonth() - date1.getMonth());

    fieldNames = {
      'NRIC': fields['NRIC'],
      'Name': fields['Name'],
      'DOB': `${fields['NRIC'].slice(4, 6)}-${fields['NRIC'].slice(2, 4)}-20${fields['NRIC'].slice(0, 2)}`,
      'Address': fields['Address'].match(regex)[1],
      'Postcode': fields['Address'].match(regex)[2],
      'State': fields['Address'].match(regex)[4],
      'numOfYear': fields['No of year in residence'],
      'Phone Number': fields['Phone Number'],
      'Email': fields['Email'],
      'Position': fields['Position'],
      'Gross Salary': fields['Gross Salary'],
      'Year of Work': `${Math.floor(totalMonths / 12)} years ${totalMonths % 12} months`,
      'Company Address': fields['Company Address'],
      'Company Phone Number': fields['Company Phone Number'],
      'Company Name': fields['Company Name'],
      'Reference Contact Name 1': referenceContact[0]['Name'],
      'Reference Contact Address 1': referenceContact[0]['Stay with user'] === 'Yes' ? fields['Address'] : referenceContact[0]['Stay where(If no)'],
      'Relation 1': referenceContact[0]['Relation to user'],
      'Reference Phone 1': referenceContact[0]['Phone Number'],
      'Reference Contact Name 2': referenceContact[1]['Name'],
      'Reference Contact Address 2': referenceContact[1]['Stay with user'] === 'Yes' ? fields['Address'] : referenceContact[1]['Stay where(If no)'],
      'Relation 2': referenceContact[1]['Relation to user'],
      'Reference Phone 2': referenceContact[1]['Phone Number'],
      'Gender': parseInt(fields['NRIC']) % 2 === 1 ? 'Male' : 'Female',
      'Ownership Status': checkOwnershipStatus(fields['Ownership Status']),
      'Ownership Status Input': '' ? checkOwnershipStatus(fields['Ownership Status']) === 'Other' : fields['Ownership Status'],
    }

    const sourcePdfPath = '/Development/Automation/BSNC/NEW BSNC FORM (1).pdf';
    const targetPdfPath = `/Development/Automation/BSNC/${nric}.pdf`;

    pdfFillForm.write(sourcePdfPath, fieldNames, { save: 'pdf', cores: 2 })
      .then((result) => {
        fs.writeFileSync(targetPdfPath, result);
        console.log('PDF filled successfully!');
      })
      .catch((error) => {
        console.log('Error:', error);
      });
    connection.end();
  })
})
