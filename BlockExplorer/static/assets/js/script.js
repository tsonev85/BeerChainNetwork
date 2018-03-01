var node = node_url;
$(function() {
    init_search_bar();
    onPageLoad();
    $('.company_name_logo').click(onPageLoad);
    $('.peers_btn').click(showPeers);
    $('.pending_transactions_btn').click(showPendingTransactions);
    $('.search_btn').click(searchButton);
});

function onPageLoad() {
    $('.search_field').val('');
    var data_table = $("#table_data");
    data_table.empty();
    var request_data = {
	   from_index: '-20',
	   to_index: 'None'
    };
    $.ajax({
        type: "POST",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        url:node + '/get_blocks_range',
        data: JSON.stringify(request_data),
        success: function(result) {
            data_table.append('<thead><tr><th>Blocks</th></tr></thead>');
            data_table.append('<thead>'+
                                '<tr>' +
                                    '<th>Block #</th>'+
                                    '<th>Block Hash</th>'+
                                    '<th>Transactions</th>'+
                                    '<th>Block Date</th>'+
                                    '<th>Mined By</th>'+
                                '</tr>'+
                              '</thead>');
            var tbody = $('<tbody>');
            data_table.append(tbody);
            for (var i = result.length-1; i >= 0; i--) {
                var block = result[i];
                var row = $('<tr>');
                var td_index = $('<td>');
                td_index.text('Block ' + block['index']);
                var td_block_hash = $('<td>');
                td_block_hash.text(block['miner_hash']);
                var td_block_transactions = $('<td>');
                td_block_transactions.text(block['transactions'].length);
                var td_block_date = $('<td>');
                var d = new Date(1970,0,1);
                d.setSeconds(block['date_created']);
                td_block_date.text(d);
                td_block_mined_by = $('<td>');
                td_block_mined_by.text(block['miner_name']);
                row.append(td_index);
                row.append(td_block_hash);
                row.append(td_block_transactions);
                row.append(td_block_date);                
                row.append(td_block_mined_by);
                tbody.append(row);
            }
        }
    });
}

function init_search_bar() {
    var search_field = $('.search_field');
    var option_select = $('.selection');
    option_select.change(function() {
        var option = option_select.val();
        var placeholder = '';
        if (option == 'Block') {
            placeholder = 'index / hash'
        } else {
            placeholder = 'hash'
        }
        search_field.attr("placeholder", placeholder);
    });
    search_field.attr("placeholder", 'index / hash');
}

function showPeers() {
    var data_table = $("#table_data");
    data_table.empty();
    $.ajax({
        type: "GET",
        dataType: "json",
        url:node + '/peers',
        success: function(result) {
            data_table.append('<thead><tr><th>Peers</th></tr></thead>');
            data_table.append('<thead>'+
                                '<tr>' +
                                    '<th>Peer ID</th>'+
                                    '<th>Peer Addres</th>'+
                                '</tr>'+
                              '</thead>');
            var tbody = $('<tbody>');
            data_table.append(tbody);
            for (var i = 0; i < result.peers.length; i++) {
                var peer = result.peers[i];
                var row = $('<tr>');
                var peer_id = $('<td>');
                peer_id.text(peer['node_identifier']);
                var peer_address = $('<td>');
                peer_address.text(peer['peer']);
                row.append(peer_id);
                row.append(peer_address);
                tbody.append(row);
            }
        }
    });   
}

function showPendingTransactions() {
    var data_table = $("#table_data");
    data_table.empty();
    $.ajax({
        type: "GET",
        dataType: "json",
        url:node + '/pending_transactions',
        success: function(result) {
            data_table.append('<thead><tr><th>Pending Transactions</th></tr></thead>');
            data_table.append('<thead>'+
                                '<tr>' +
                                    '<th>Transaction Hash</th>'+
                                    '<th>From Address</th>'+
                                    '<th>To Address</th>'+
                                    '<th>Amount</th>'+
                                '</tr>'+
                              '</thead>');
            var tbody = $('<tbody>');
            data_table.append(tbody);
            for (var i = 0; i < result.pendingTransactions.length; i++) {
                var transaction = result.pendingTransactions[i];
                var row = $('<tr>');
                var transaction_id = $('<td>');
                transaction_id.text(transaction['transaction_hash']);
                var from_address = $('<td>');
                from_address.text(transaction['from_address']);
                var to_address = $('<td>');
                to_address.text(transaction['to_address']);
                var amount = $('<td>');
                amount.text(transaction['value']);
                row.append(transaction_id);
                row.append(from_address);
                row.append(to_address);
                row.append(amount);
                tbody.append(row);
            }
        }
    });
}

function searchButton() {
    var search_field = $('.search_field');
    var option_select = $('.selection');
    switch(option_select.val()) {
        case 'Block':
            searchBlock(search_field.val());
            break;
        case 'Transaction':
            searchTransaction(search_field.val());
            break;
        case 'Account':
            searchAccount(search_field.val());
            break;
        default:
            break;
    }
    search_field.val('');
}

function searchBlock(blockId) {
    var block_url = '/get_block_by_index';
    var request_data = {
	   index: blockId
    };
    if (blockId % 1 != 0) {
        block_url = '/get_block_by_hash'; 
        request_data = {
            hash: blockId
        };
    }
    var data_table = $("#table_data");
    data_table.empty();
    function appendElement(el, title, text){
        var row = $('<tr>');
        
        var _title = $('<td>');
        _title.text(title);
        _title.css("font-weight","Bold");
        var _text = $('<td>');
        _text.text(text);
        row.append(_title);
        row.append(_text);
        
        el.append(row);
    };
    
    function calculateBlockValue(block) {
        var value = 0;
        
        for (var i = 0 ; i < block.transactions.length; i++) {
            var transaction = block.transactions[i];
            value += transaction.value;
        }
        
        return value;
    };
    
    $.ajax({
        type: "POST",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        url:node + block_url,
        data: JSON.stringify(request_data),
        success: function(result) {
            if (result == null) {
                data_table.append('<thead><tr><th>Block not found!</th></tr></thead>');
                return;
            }
            var block = result;
            data_table.append('<thead><tr><th>Block '+ block.index +'</th></tr></thead>');
            var tbody = $('<tbody>');
            data_table.append(tbody);           
            appendElement(tbody, 'Index: ', block.index);
            appendElement(tbody, 'Hash: ', block.miner_hash);
            appendElement(tbody, 'Prev hash: ', block.prev_block_hash);
            appendElement(tbody, 'Nonce: ', block.nonce);
            appendElement(tbody, 'Difficulty: ', block.difficulty);
            var d = new Date(1970,0,1);
            d.setSeconds(block.date_created);
            appendElement(tbody, 'Block date: ', d);
            appendElement(tbody, 'Mined by: ', block.miner_name);
            appendElement(tbody, 'Block value: ', calculateBlockValue(block));
            appendElement(tbody, 'Transactions in block: ', block.transactions.length);
            appendElement(tbody, ' ');
            for (var i = 0 ; i < block.transactions.length; i++) {
                var transaction = block.transactions[i];
                appendElement(tbody, '  Transaction: ', transaction.transaction_hash);
                appendElement(tbody, '  From Address: ', transaction.from_address);
                appendElement(tbody, '  To Address: ', transaction.to_address);
                appendElement(tbody, '  Value: ', transaction.value);
                appendElement(tbody, '  Status: ', (transaction.paid == true) ? "Paid" : "Not Paid");
                appendElement(tbody, ' ');
            }
        }
    });
}

function searchAccount(accountId) {
    var data_table = $("#table_data");
    data_table.empty();
    $.ajax({
        type: "GET",
        dataType: "json",
        url:node + '/get_last_block',
        success: function(result) {
            var accounts = result.current_state_balances;
            if (accounts[accountId] == undefined) {
                data_table.append('<thead><tr><th>No account found!</th></tr></thead>');
                return;
            }
            data_table.append('<thead><tr><th>Account Infromation</th></tr></thead>');
            data_table.append('<thead>'+
                                '<tr>' +
                                    '<th>Account</th>'+
                                    '<th>Balance</th>'+
                                '</tr>'+
                              '</thead>');
            var tbody = $('<tbody>');
            data_table.append(tbody);
            var row = $('<tr>');
            var account_id = $('<td>');
            account_id.text(accountId);
            var account_balance = $('<td>');
            account_balance.text(accounts[accountId]);
            row.append(account_id);
            row.append(account_balance);
            tbody.append(row);
        }
    });
}

function searchTransaction(transactionId) {
    var data_table = $("#table_data");
    data_table.empty();
    
    function appendElement(el, title, text){
        var row = $('<tr>');
        
        var _title = $('<td>');
        _title.text(title);
        _title.css("font-weight","Bold");
        var _text = $('<td>');
        _text.text(text);
        row.append(_title);
        row.append(_text);
        
        el.append(row);
    };
    
    var request_data = {
	   hash: transactionId
    };
    
    $.ajax({
        type: "POST",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        url:node + "/get_transaction_by_hash",
        data: JSON.stringify(request_data),
        success: function(result) {
            if ($.isEmptyObject(result)) {
                data_table.append('<thead><tr><th>Transaction not found!</th></tr></thead>');
                return;
            }
            var transaction = result;
            data_table.append('<thead><tr><th>Transaction Information</th></tr></thead>');
            var tbody = $('<tbody>');
            data_table.append(tbody);
            appendElement(tbody, '  Transaction: ', transaction.transaction_hash);
            appendElement(tbody, '  From Address: ', transaction.from_address);
            appendElement(tbody, '  To Address: ', transaction.to_address);
            appendElement(tbody, '  Value: ', transaction.value);
            appendElement(tbody, '  Status: ', (transaction.paid == true) ? "Paid" : "Not Paid");
            var d = new Date(1970,0,1);
            d.setSeconds(transaction.date_created);
            appendElement(tbody, '  Date created: ', d);
            var block_index = transaction.mined_in_block_index;
            if (block_index == null) {
                block_index = 'Pending';
            }
            appendElement(tbody, '  Mined in block: ', block_index);
            appendElement(tbody, '  Sender public key: ', transaction.sender_pub_key);
            appendElement(tbody, '  Transaction signature: ', transaction.sender_signature);
            appendElement(tbody, ' ');
        }
    });
}