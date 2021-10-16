
#include "moyo_ble.h"
#include "nordic_common.h"
#include "ble_srv_common.h"
#include "app_util.h"
#include "nrf_log.h"

static void on_connect(ble_moyo_t * p_moyo, ble_evt_t const * p_ble_evt)
{
    p_moyo->conn_handle = p_ble_evt->evt.gap_evt.conn_handle;
    //ble_moyo_update(p_moyo);
}

static void on_disconnect(ble_moyo_t * p_moyo, ble_evt_t const * p_ble_evt)
{
    UNUSED_PARAMETER(p_ble_evt);
    p_moyo->conn_handle = BLE_CONN_HANDLE_INVALID;
}

/**@brief Function for handling the Write event.
 *
 * @param[in]   p_moyo   LED Button Service structure.
 * @param[in]   p_ble_evt        Event received from the BLE stack.
 */

void ble_moyo_on_ble_evt(ble_moyo_t * p_moyo, ble_evt_t const * p_ble_evt)
{
     
    NRF_LOG_INFO("BLE event received. Event type = %d\r\n", p_ble_evt->header.evt_id); 
 
    if (p_moyo == NULL || p_ble_evt == NULL)
    {
        return;
    }
 
    switch (p_ble_evt->header.evt_id)
    {
        case BLE_GAP_EVT_CONNECTED:
            on_connect(p_moyo, p_ble_evt);
            break;
            
        case BLE_GAP_EVT_DISCONNECTED:
            on_disconnect(p_moyo, p_ble_evt);
            break;
            
        default:
            // No implementation needed.
            break;
    }
}

uint32_t ble_moyo_char_add(ble_moyo_t * p_moyo, ble_moyo_init_t const * p_moyo_init)
{
    uint32_t            err_code;
    ble_gatts_char_md_t char_md;
    ble_gatts_attr_md_t cccd_md;
    ble_gatts_attr_t    attr_char_value;
    ble_uuid_t          ble_uuid;
    ble_gatts_attr_md_t attr_md;



    memset(&cccd_md, 0, sizeof(cccd_md));
    /* No protection, open link. */
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    cccd_md.vloc = BLE_GATTS_VLOC_STACK;

    /* Connection proporties */
    memset(&char_md, 0, sizeof(char_md));
    char_md.char_props.read          = 1;
    char_md.char_props.write_wo_resp = 0;
    char_md.char_props.notify        = 0;
    char_md.p_char_user_desc         = NULL;
    char_md.p_char_pf                = NULL;
    char_md.p_user_desc_md           = NULL;
    char_md.p_cccd_md                = &cccd_md;
    char_md.p_sccd_md                = NULL;

    /* Heart Rate characteristics */
    ble_uuid.type                    = BLE_UUID_TYPE_BLE;
    ble_uuid.uuid                    = BLE_UUID_MOYO_HR;
    memset(&attr_md, 0, sizeof(attr_md));
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.write_perm);
    attr_md.vloc       = BLE_GATTS_VLOC_STACK;
    attr_md.rd_auth    = 0;
    attr_md.wr_auth    = 0;
    attr_md.vlen       = 0;

    memset(&attr_char_value, 0, sizeof(attr_char_value));
    attr_char_value.p_uuid       = &ble_uuid;
    attr_char_value.p_attr_md    = &attr_md;
    attr_char_value.init_len     = sizeof(uint8_t);
    attr_char_value.init_offs    = 0;
    attr_char_value.max_len      = sizeof(uint8_t);   /**> Must be in size of moyo_data.hr_data */
    attr_char_value.p_value      = NULL;

    err_code= sd_ble_gatts_characteristic_add(p_moyo->service_handle, &char_md,
                                           &attr_char_value,
                                           &p_moyo->moyo_hr_handle);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }
    
  
    /* Temperature characteristics */
    memset(&cccd_md, 0, sizeof(cccd_md));
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    cccd_md.vloc = BLE_GATTS_VLOC_STACK;

    memset(&char_md, 0, sizeof(char_md));
    char_md.char_props.read          = 1;
    char_md.char_props.write_wo_resp = 0;
    char_md.char_props.notify        = 0;
    char_md.p_char_user_desc         = NULL;
    char_md.p_char_pf                = NULL;
    char_md.p_user_desc_md           = NULL;
    char_md.p_cccd_md                = &cccd_md;
    char_md.p_sccd_md                = NULL;

    ble_uuid.type                    = BLE_UUID_TYPE_BLE;
    ble_uuid.uuid                    = BLE_UUID_MOYO_TEMPERATURE;
    
    memset(&attr_md, 0, sizeof(attr_md));
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.write_perm);
    attr_md.vloc       = BLE_GATTS_VLOC_STACK;
    attr_md.rd_auth    = 0;
    attr_md.wr_auth    = 0;
    attr_md.vlen       = 0;

    memset(&attr_char_value, 0, sizeof(attr_char_value));
    attr_char_value.p_uuid       = &ble_uuid;
    attr_char_value.p_attr_md    = &attr_md;
    attr_char_value.init_len     = sizeof(uint16_t);
    attr_char_value.init_offs    = 0;
    attr_char_value.max_len      = sizeof(uint16_t);    /**> Must be in size of moyo_data.temperature */
    attr_char_value.p_value      = NULL;

    err_code= sd_ble_gatts_characteristic_add(p_moyo->service_handle, &char_md,
                                           &attr_char_value,
                                           &p_moyo->moyo_temperature_handle);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    
    /* Oximetry characteristics */
    memset(&cccd_md, 0, sizeof(cccd_md));
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    cccd_md.vloc = BLE_GATTS_VLOC_STACK;

    memset(&char_md, 0, sizeof(char_md));
    char_md.char_props.read          = 1;
    char_md.char_props.write_wo_resp = 0;
    char_md.char_props.notify        = 0;
    char_md.p_char_user_desc         = NULL;
    char_md.p_char_pf                = NULL;
    char_md.p_user_desc_md           = NULL;
    char_md.p_cccd_md                = &cccd_md;
    char_md.p_sccd_md                = NULL;

    ble_uuid.type                    = BLE_UUID_TYPE_BLE;
    ble_uuid.uuid                    = BLE_UUID_MOYO_OXIMETRY;
    
    memset(&attr_md, 0, sizeof(attr_md));
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.write_perm);
    attr_md.vloc       = BLE_GATTS_VLOC_STACK;
    attr_md.rd_auth    = 0;
    attr_md.wr_auth    = 0;
    attr_md.vlen       = 0;

    memset(&attr_char_value, 0, sizeof(attr_char_value));
    attr_char_value.p_uuid       = &ble_uuid;
    attr_char_value.p_attr_md    = &attr_md;
    attr_char_value.init_len     = sizeof(uint8_t);
    attr_char_value.init_offs    = 0;
    attr_char_value.max_len      = sizeof(uint8_t);     /**> Must be in size of moyo_data.oximetry */
    attr_char_value.p_value      = NULL;
    
    return sd_ble_gatts_characteristic_add(p_moyo->service_handle, &char_md,
                                           &attr_char_value,
                                           &p_moyo->moyo_oximetry_handle);
}

uint32_t ble_moyo_init(ble_moyo_t * p_moyo, const ble_moyo_init_t * p_moyo_init)
{
    uint32_t   err_code;
    ble_uuid_t ble_uuid;

    p_moyo->conn_handle = BLE_CONN_HANDLE_INVALID;
    p_moyo->evt_handler = p_moyo_init->evt_handler;

    ble_uuid.type = BLE_UUID_TYPE_BLE;
    ble_uuid.uuid = BLE_UUID_MOYO_SERVICE_UUID;
    
    err_code = sd_ble_gatts_service_add(BLE_GATTS_SRVC_TYPE_PRIMARY, &ble_uuid, &p_moyo->service_handle);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    err_code = ble_moyo_char_add(p_moyo, p_moyo_init);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    return  NRF_SUCCESS;
}

uint32_t ble_moyo_update(ble_moyo_t * p_moyo)
{
    NRF_LOG_INFO("Updating BLE values");
    if (p_moyo == NULL)
    {
        return NRF_ERROR_NULL;
    }
    uint32_t err_code = NRF_SUCCESS;
    ble_gatts_value_t gatts_value;

    /* Update Heart Rate */
    memset(&gatts_value, 0, sizeof(gatts_value));

    gatts_value.len     = sizeof(uint8_t);
    gatts_value.offset  = 0;
    gatts_value.p_value = &p_moyo->moyo_data.hr_data;

    err_code = sd_ble_gatts_value_set(p_moyo->conn_handle,
                                      p_moyo->moyo_hr_handle.value_handle,
                                      &gatts_value);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }

    /* Update Oximetry */
    memset(&gatts_value, 0, sizeof(gatts_value));

    gatts_value.len     = sizeof(uint8_t);
    gatts_value.offset  = 0;
    gatts_value.p_value = &p_moyo->moyo_data.oximetry;

    err_code = sd_ble_gatts_value_set(p_moyo->conn_handle,
                                      p_moyo->moyo_oximetry_handle.value_handle,
                                      &gatts_value);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }
    
    /* Update Temperature */
    memset(&gatts_value, 0, sizeof(gatts_value));

    gatts_value.len     = sizeof(uint16_t);
    gatts_value.offset  = 0;
    gatts_value.p_value = &p_moyo->moyo_data.temperature;

    err_code = sd_ble_gatts_value_set(p_moyo->conn_handle,
                                      p_moyo->moyo_temperature_handle.value_handle,
                                      &gatts_value);
    if (err_code != NRF_SUCCESS)
    {
        return err_code;
    }
    NRF_LOG_INFO("Updating BLE values done");
    return err_code;
}
