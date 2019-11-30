function setFormId(form, number) {
    let formId = 'form-' + number;
    form.attr('id', formId);

    let select = form.find('select');
    select.attr('name', formId + '-product');

    let inputs = form.find('input');

    let amountInput = $(inputs[0]);
    amountInput.attr('name', formId + '-amount');

    let idInput = $(inputs[1]);
    idInput.attr('name', formId + '-id');

    let deleteButton = form.find('.btn-danger');
    deleteButton.data('id', '#' + formId);
}

function addProductForm (event) {
    let totalFormsInput = $("#id_form-TOTAL_FORMS");
    let maxFormsInput = $("#id_form-MAX_NUM_FORMS");
    let totalForms = totalFormsInput.val();
    let maxForms = maxFormsInput.val();
    if(totalForms === maxForms) {
        alert('Максимальное количество товаров добавлено!');
    } else {
        let formTemplate =$("#product_forms .form-row").first().clone();

        setFormId(formTemplate, totalForms);

        let select = formTemplate.find('select');
        select.val('');

        let deleteButton = formTemplate.find('.btn-danger');
        deleteButton.click(deleteProductForm);

        let inputs = formTemplate.find('input');

        let amountInput = $(inputs[0]);
        amountInput.val('');

        let idInput = $(inputs[1]);
        idInput.val('');

        let errors = formTemplate.find('p.text-danger');
        errors.remove();

        $("#product_forms").append(formTemplate);

        totalFormsInput.val(parseInt(totalForms) + 1);
    }
}

function deleteProductForm(event) {
    let totalFormsInput = $("#id_form-TOTAL_FORMS");
    let minFormsInput = $("#id_form-MIN_NUM_FORMS");
    let totalForms = totalFormsInput.val();
    let minForms = minFormsInput.val();
    if(totalForms === minForms) {
        alert('В заказе должен быть хотя бы ' + minForms + " товар(а/ов).");
    } else {
        let formId = $(event.target).data('id');
        let form = $(formId);

        form.remove();

        totalFormsInput.val(parseInt(totalForms) - 1);

        let forms = $("#product_forms .form-row");
        for(let i = 0; i < totalForms; i++) {
            setFormId($(forms[i]), i);
        }
    }
}

$(document).ready(function() {
    $('#add_product_form').click(addProductForm);
    $('#product_forms button.btn-danger').click(deleteProductForm)
});
